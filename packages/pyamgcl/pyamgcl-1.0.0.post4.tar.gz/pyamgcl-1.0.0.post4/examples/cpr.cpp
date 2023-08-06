#include <iostream>
#include <string>

#include <boost/program_options.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/foreach.hpp>

#include <amgcl/make_solver.hpp>
#include <amgcl/runtime.hpp>
#include <amgcl/preconditioner/cpr.hpp>
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
    tic t1(prof, "CPR");

    typedef amgcl::backend::builtin<double> Backend;

    typedef
        amgcl::runtime::amg<Backend>
        PPrecond;

    typedef
        amgcl::runtime::relaxation::as_preconditioner<Backend>
        SPrecond;

    amgcl::make_solver<
        amgcl::preconditioner::cpr<PPrecond, SPrecond>,
        amgcl::runtime::iterative_solver<Backend>
        > solve(K, prm);

    std::cout << solve.precond() << std::endl;

    tic t2(prof, "solve");
    std::vector<double> x(rhs.size(), 0.0);

    size_t iters;
    double error;

    boost::tie(iters, error) = solve(rhs, x);

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
    vector<double> val, rhs;
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
    }

    solve_cpr(boost::tie(rows, ptr, col, val), rhs, prm);

    std::cout << prof << std::endl;
}
