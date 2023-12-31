# pySigma panther_sdyaml Backend

[![Test](https://github.com/panther-labs/pySigma-backend-panther-sdyaml/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/panther-labs/pySigma-backend-panther-sdyaml/actions/workflows/test.yml)
![Status](https://img.shields.io/badge/Status-pre--release-orange)

[Docs](https://docs.panther.com/panther-developer-workflows/converting-sigma-rules)

This is the `panther_python` backend for pySigma. It provides the package `sigma.backends.panther` with the `PantherSdYamlBackend` class.

It supports the following output formats:

* default: [Panther YAML Detections](https://docs.panther.com/detections/rules/yaml#simple-detections) format

To save each rule in separate file you can use `output_dir` backend option.
> $ sigma convert -t panther_sdyaml path/to/rules -p panther_sdyaml -O output_dir=output/directory

Further, it contains the following processing pipelines in `sigma.pipelines.panther_sdyaml`:

* panther_sdyaml_pipeline: Convert known Sigma field names into their Panther schema equivalent

### Local setup for development
Clone this repo, cd into it and run:
```poetry install```
that is all you need to do. 

Now you can run tests with:
```poetry run pytest```

To convert rules to panther sdyaml format run:
```poetry run sigma convert -t panther_sdyaml -p panther_sdyaml path_to_sigma_rule.yml```

This backend is currently maintained by:

* [Oleh Melenevskyi](https://github.com/melenevskyi/)
