{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
			packages = rec {
				website = pkgs.stdenvNoCC.mkDerivation {
					pname = "lemmy-atlas-website";
					version = "TODO-use-git";

					dontUnpack = true;

					installPhase = ''
						mkdir -p $out
						cp -r ${./web}/* $out/
					'';
				};
				default = website;
			};
		}
  );
}