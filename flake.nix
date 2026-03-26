# This flake provides a skeleton dev environment for PyTorch with CUDA support and for CUDA deevlopment /
# compilation with NVCC.
#
# To test python:
# $ nix develop
# $ python
# >>> import torch
# >>> torch.cuda.is_available()
# >>> torch.cuda.device_count()
# >>> torch.cuda.get_device_name(0)
#
# To test CUDA (hello-world.cu):
# $ nix develop
# $ nvcc hello-world.cu -o hello
# $ ./hello

{
  description = "A flake providing a dev shell for PyTorch with CUDA and CUDA development using NVCC.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux"; # Adjust if needed
      pkgs = import nixpkgs {
        system = system;
        config.allowUnfree = true;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell rec {
        buildInputs = with pkgs; [
          python3
          (python3.withPackages (
            ps: with ps; [
              python-dotenv 
              pyoxigraph 
              pandas 
              tqdm 
              networkx 
              pyvis 
              matplotlib 
              pytest 
              openpyxl 
              pint 
              plotly 
              kaleido
              openai
              torchWithCuda
              (ps.buildPythonPackage rec {
                pname = "qlever";
                version = "0.5.44";
                format = "pyproject";

                src = pkgs.fetchPypi {
                  inherit pname;
                  inherit version;
                  hash = "sha256-1GHZtbPQlwBTmkvr6qRUw3mfcK9BWbW3JCEjZit+6jk="; # fill after first run
                };
                nativeBuildInputs = [ setuptools poetry-core ];
                propagatedBuildInputs = [
                  psutil
                  termcolor
                  argcomplete
                  pyyaml
                  rdflib
                  tqdm
                  (ps.buildPythonPackage rec {
                    pname = "requests-sse";
                    version = "";
                    format = "pyproject";

                    src = pkgs.fetchFromGitHub {
                      owner = "overcat";
                      repo = pname;
                      rev = "main";
                      hash = "sha256-HE4N3D6WveJtDw9In6v9Pwoi6RuXPCDi8rn1vywILTs="; # fill after first run
                    };
                    nativeBuildInputs = [ setuptools poetry-core ];
                    propagatedBuildInputs = [ requests ];
                  })
                ];
              })
              (ps.buildPythonPackage rec {
                pname = "streamlit-searchbox";
                version = "0.1.24";
                format = "pyproject";

                src = pkgs.fetchurl {
                  url = "https://files.pythonhosted.org/packages/46/c1/b037f76f7d6da73af6311720df3c56ed534616572da4261c0dea1e37110e/streamlit_searchbox-0.1.24.tar.gz";
                  sha256 = "sha256-tgCcNogS/uoN0hHwPJzFzIW1QLDQpXFluyiF9n1qij0=";

                };
                nativeBuildInputs = [ setuptools ];
                propagatedBuildInputs = [ streamlit ];
              })
              (ps.buildPythonPackage rec {
                pname = "wikirate4py";
                version = "2.0.5";
                format = "setuptools";

                src = pkgs.fetchFromGitHub {
                  owner = "wikirate";
                  repo = pname;
                  rev = "main";

                  hash = "sha256-kwlsuU0Er1gV1QLx5sqcK45LJQQG8d8XgY4lNEYdV8I="; # fill after first run
                };
                propagatedBuildInputs = [
                  html2text
                ];
              })
            ]
          ))
          cudatoolkit
          cudaPackages.cudnn
          cudaPackages.cuda_cudart

          # Need to explicitly override the system gcc (gcc14 in this case) as CUDA requires a
          # lower version for compatibility
          gcc13
        ];

        shellHook = ''
          export CUDA_PATH=${pkgs.cudatoolkit}

          # Set CC to GCC 13 to avoid the version mismatch error
          export CC=${pkgs.gcc13}/bin/gcc
          export CXX=${pkgs.gcc13}/bin/g++
          export PATH=${pkgs.gcc13}/bin:$PATH

          # Add necessary paths for dynamic linking
          export LD_LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath ([
              "/run/opengl-driver" # Needed to find libGL.so
            ] ++ buildInputs)
          }:$LD_LIBRARY_PATH

          # Set LIBRARY_PATH to help the linker find the CUDA static libraries
          export LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath [
              pkgs.cudatoolkit
            ]
          }:$LIBRARY_PATH

          eval "$(register-python-argcomplete qlever)" && export QLEVER_ARGCOMPLETE_ENABLED=1
        '';
      };
    };
}
