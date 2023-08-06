#include <iostream>
#include <string>

#include <boost/program_options.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/foreach.hpp>

#if defined(SOLVER_BACKEND_VEXCL)
#  include <amgcl/backend/vexcl.hpp>
   typedef amgcl::backend::vexcl<double> Backend;
#elif defined(SOLVER_BACKEND_VIENNACL)
#  include <amgcl/backend/viennacl.hpp>
   typedef amgcl::backend::viennacl< viennacl::compressed_matrix<double> > Backend;
#elif defined(SOLVER_BACKEND_CUDA)
#  include <amgcl/backend/cuda.hpp>
#  include <amgcl/relaxation/cusparse_ilu0.hpp>
   typedef amgcl::backend::cuda<double> Backend;
#else
#  ifndef SOLVER_BACKEND_BUILTIN
#    define SOLVER_BACKEND_BUILTIN
#  endif
#  include <amgcl/backend/builtin.hpp>
   typedef amgcl::backend::builtin<double> Backend;
#endif

#include <amgcl/make_solver.hpp>
#include <amgcl/runtime.hpp>
#include <amgcl/preconditioner/cpr_drs.hpp>
#include <amgcl/adapter/crs_tuple.hpp>
#include <amgcl/io/mm.hpp>
#include <amgcl/io/binary.hpp>
#include <amgcl/profiler.hpp>

namespace amgcl { profiler<> prof; }
using amgcl::prof;
using amgcl::precondition;

typedef amgcl::scoped_tic< amgcl::profiler<> > tic;

//---------------------------------------------------------------------------
template <class Matrix>
void solve_cpr(const Matrix &K, const std::vector<double> &rhs, boost::property_tree::ptree &prm)
{
    Backend::params bprm;

#if defined(SOLVER_BACKEND_VEXCL)
    vex::Context ctx(vex::Filter::Env);
    std::cout << ctx << std::endl;
    bprm.q = ctx;
#elif defined(SOLVER_BACKEND_VIENNACL)
    std::cout
        << viennacl::ocl::current_device().name()
        << " (" << viennacl::ocl::current_device().vendor() << ")\n\n";
#elif defined(SOLVER_BACKEND_CUDA)
    cusparseCreate(&bprm.cusparse_handle);
    {
        int dev;
        cudaGetDevice(&dev);

        cudaDeviceProp prop;
        cudaGetDeviceProperties(&prop, dev);
        std::cout << prop.name << std::endl << std::endl;
    }
#endif

    tic t1(prof, "CPR");

    typedef
        amgcl::runtime::amg<Backend>
        PPrecond;

    typedef
        amgcl::runtime::relaxation::as_preconditioner<Backend>
        SPrecond;

    amgcl::make_solver<
        amgcl::preconditioner::cpr_drs<PPrecond, SPrecond>,
        amgcl::runtime::iterative_solver<Backend>
        > solve(K, prm, bprm);

    std::cout << solve.precond() << std::endl;

    typedef Backend::vector vector;
    boost::shared_ptr<vector> f = Backend::copy_vector(rhs, bprm);
    boost::shared_ptr<vector> x = Backend::create_vector(rhs.size(), bprm);
    amgcl::backend::clear(*x);

    tic t2(prof, "solve");
    size_t iters;
    double error;

    boost::tie(iters, error) = solve(*f, *x);

    std::cout << "Iterations: " << iters << std::endl
              << "Error:      " << error << std::endl;
}

//---------------------------------------------------------------------------
int main(int argc, char *argv[]) {
    using std::string;
    using std::vector;
    using amgcl::prof;
    using amgcl::precondition;

    namespace po = boost::program_options;
    namespace io = amgcl::io;

    po::options_description desc("Options");

    desc.add_options()
        ("help,h", "show help")
        (
         "binary,B",
         po::bool_switch()->default_value(false),
         "When specified, treat input files as binary instead of as MatrixMarket. "
         "It is assumed the files were converted to binary format with mm2bin utility. "
        )
        (
         "matrix,A",
         po::value<string>()->required(),
         "The system matrix in MatrixMarket format"
        )
        (
         "rhs,f",
         po::value<string>(),
         "The right-hand side in MatrixMarket format"
        )
        (
         "weights,w",
         po::value<string>(),
         "Equation weights in MatrixMarket format"
        )
        (
         "block-size,b",
         po::value<int>(),
         "The block size of the system matrix"
        )
        (
         "params,P",
         po::value<string>(),
         "parameter file in json format"
        )
        (
         "prm,p",
         po::value< vector<string> >()->multitoken(),
         "Parameters specified as name=value pairs. "
         "May be provided multiple times. Examples:\n"
         "  -p solver.tol=1e-3\n"
         "  -p precond.coarse_enough=300"
        )
        ;

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);

    if (vm.count("help")) {
        std::cout << desc << std::endl;
        return 0;
    }

    po::notify(vm);

    boost::property_tree::ptree prm;
    if (vm.count("params")) read_json(vm["params"].as<string>(), prm);

    if (vm.count("prm")) {
        BOOST_FOREACH(string pair, vm["prm"].as<vector<string> >())
        {
            using namespace boost::algorithm;
            vector<string> key_val;
            split(key_val, pair, is_any_of("="));
            if (key_val.size() != 2) throw po::invalid_option_value(
                    "Parameters specified with -p option "
                    "should have name=value format");

            prm.put(key_val[0], key_val[1]);
        }
    }

    if (vm.count("block-size"))
        prm.put("precond.block_size", vm["block-size"].as<int>());

    size_t rows;
    vector<ptrdiff_t> ptr, col;
    vector<double> val, rhs, wgt;
    std::vector<char> pm;

    {
        tic t(prof, "reading");

        string Afile  = vm["matrix"].as<string>();
        bool   binary = vm["binary"].as<bool>();

        if (binary) {
            io::read_crs(Afile, rows, ptr, col, val);
        } else {
            size_t cols;
            boost::tie(rows, cols) = io::mm_reader(Afile)(ptr, col, val);
            precondition(rows == cols, "Non-square system matrix");
        }

        if (vm.count("rhs")) {
            string bfile = vm["rhs"].as<string>();

            size_t n, m;

            if (binary) {
                io::read_dense(bfile, n, m, rhs);
            } else {
                boost::tie(n, m) = io::mm_reader(bfile)(rhs);
            }

            precondition(n == rows && m == 1, "The RHS vector has wrong size");
        } else {
            rhs.resize(rows, 1.0);
        }

        if (vm.count("weights")) {
            string wfile = vm["weights"].as<string>();

            size_t n, m;

            if (binary) {
                io::read_dense(wfile, n, m, wgt);
            } else {
                boost::tie(n, m) = io::mm_reader(wfile)(wgt);
            }

            prm.put("precond.weights",      &wgt[0]);
            prm.put("precond.weights_size", wgt.size());
        }
    }

    solve_cpr(boost::tie(rows, ptr, col, val), rhs, prm);

    std::cout << prof << std::endl;
}
