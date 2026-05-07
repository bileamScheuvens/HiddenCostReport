{
  description = "Environment definition for hiddencostreport.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
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
              (ps.buildPythonPackage rec {
                pname = "qlever";
                version = "0.5.44";
                format = "pyproject";

                src = pkgs.fetchPypi {
                  inherit pname;
                  inherit version;
                  hash = "sha256-1GHZtbPQlwBTmkvr6qRUw3mfcK9BWbW3JCEjZit+6jk="; # fill after first run
                };
                nativeBuildInputs = [
                  setuptools
                  poetry-core
                ];
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
                      hash = "sha256-JflM6Rx9TFS7EsusqBJViDvk3X3YAawzI75jn84cbZM="; # fill after first run
                    };
                    nativeBuildInputs = [
                      setuptools
                      poetry-core
                    ];
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

                  hash = "sha256-eHRVtvm2ELApnLXmk0CEdwZxQF6C74OVbj0DX2lEA0g="; # fill after first run
                };
                propagatedBuildInputs = [
                  html2text
                ];
              })
            ]
          ))
        ];

        shellHook = ''
          # Add necessary paths for dynamic linking
          export LD_LIBRARY_PATH=${
            pkgs.lib.makeLibraryPath (
              [
                "/run/opengl-driver" # Needed to find libGL.so
              ]
              ++ buildInputs
            )
          }:$LD_LIBRARY_PATH

          eval "$(register-python-argcomplete qlever)" && export QLEVER_ARGCOMPLETE_ENABLED=1
        '';
      };
    };
}
