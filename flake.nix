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
					pname = "fediverse-canvas-atlas-website";
					version = "TODO-use-git";

					dontUnpack = true;

					installPhase = ''
						mkdir -p $out
						cp -r ${./.}/web/* $out/
						${pkgs.python3}/bin/python ${./.}/tools/merge_data.py ${./.}/entries $out/atlas.json
						rm $out/about.html
					'';
				};
				default = website;
			};
		}
  );
}