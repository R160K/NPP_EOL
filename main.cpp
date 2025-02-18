#include <iostream>
#include <string>
#include <vector> // for dynamic arrays
#include <cstdlib> // for launching processes
#include <thread> // for launching npp in background

void launchNPP() {
	system("notepad++");
}

int main(int argc, char* argv[]) {
	std::string TARGET_0 = "-eolwindows";
	std::string TARGET_1 = "-eolmacos";
	std::string TARGET_2 = "-eolunix";
	
	int eol_arg = -1;
	
	std::vector<std::string> pargs; // args to be passed on
	

	//Check arguments list for EOL arg
    for (int i = 0; i < argc; ++i) {
		if (argv[i] == TARGET_0) {
			// CRLF -eolwindows
			if (eol_arg < 0) {
				eol_arg = 0;
			}
		} else if (argv[i] == TARGET_1) {
			// CR -eolmacos
			if (eol_arg < 0) {
				eol_arg = 1;
			}
		} else if (argv[i] == TARGET_2) {
			// LF -eolunix
			if (eol_arg < 0) {
				eol_arg = 2;
			}
		} else {
			pargs.push_back(argv[i]);
		}
	}
	

	//Create string to launch npp
	std::string launch_code = "start notepad++";
	
	for (int i = 1; i < pargs.size(); ++i) {
		launch_code += " " + pargs[i];
	}

	

	//Launch process (npp) in background
	system(launch_code.c_str());
	
	
	//Check if custom EOL argument has been provided
	if (eol_arg >= 0) {
		std::string script_code = "start python C:/Scripts/NPP/change_eol.py " + std::to_string(eol_arg);
		system(script_code.c_str());
	}
	
	return 0;
}