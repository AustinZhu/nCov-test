from ncov_lib import nCov

if __name__ =="__main__":
    nCov_runner = nCov()
    nCov_runner.get_data()
    nCov_runner.out_json()
    nCov_runner.out_js()