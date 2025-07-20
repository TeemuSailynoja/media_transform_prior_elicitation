# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.3",
#     "pymc-marketing==0.15.0",
# ]
# ///

import marimo

__generated_with = "0.14.12"
app = marimo.App(app_title="Saturation function explorer")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Explore saturation transforms""")
    return


@app.cell(hide_code=True)
def _(SATURATION_TRANSFORMATIONS, mo):
    saturation_selector = mo.ui.dropdown(
        label="Select saturation function:",
        options=SATURATION_TRANSFORMATIONS.keys(),
        value="no_saturation",
    )
    saturation_selector
    return (saturation_selector,)


@app.cell(hide_code=True)
def _(mo, saturation_priors):
    saturation_prior_params = mo.ui.dictionary(
        label="Saturation function priors",
        elements={
            param: mo.ui.dictionary(
                label=param_prior.to_dict()["dist"],
                elements={
                    key: mo.ui.slider(
                        start=0.1 * val,
                        stop=10 * val,
                        step=0.1,
                        value=val,
                        show_value=True,
                        label=key,
                    )
                    for key, val in param_prior.to_dict()["kwargs"].items()
                },
            )
            for param, param_prior in saturation_priors.items()
        },
    ).form()
    saturation_prior_params
    return (saturation_prior_params,)


@app.cell(hide_code=True)
def _(plt, saturation_priors, updated_saturation_priors):
    _fig = plt.figure(figsize=(9, 4)).suptitle('Selected saturation function priors', fontsize=14)

    for idx, (param_name, prior) in enumerate(updated_saturation_priors.items()):
        _ax = plt.subplot(1, len(updated_saturation_priors.keys()), idx + 1)
        _ax = saturation_priors[param_name].preliz.plot_pdf(
            ax=_ax, legend=None, color="grey"
        )
        _ax = prior.preliz.plot_pdf(ax=_ax, legend="title")
        _ax.set_title(param_name + ": " + _ax.get_title())
    _ax
    return


@app.cell(hide_code=True)
def _(saturation, saturation_curve, saturation_selector):
    _fig, _ax = saturation.plot_curve_hdi(saturation_curve)
    _fig, _ax = saturation.plot_curve_hdi(
        saturation_curve, hdi_kwargs={"hdi_prob": 0.5}, axes=_ax
    )
    _fig, _ax = saturation.plot_curve(saturation_curve, axes=_ax)
    _ax[0].set_title("Saturation: " + saturation_selector.value.replace("_", " ").capitalize()
    )
    _ax[0]
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _():
    from pymc_marketing.mmm.components.saturation import SATURATION_TRANSFORMATIONS

    return (SATURATION_TRANSFORMATIONS,)


@app.cell(hide_code=True)
def _(SATURATION_TRANSFORMATIONS, saturation_selector):
    default_saturation = SATURATION_TRANSFORMATIONS[saturation_selector.value]()
    return (default_saturation,)


@app.cell(hide_code=True)
def _(default_saturation):
    saturation_priors = default_saturation.function_priors
    return (saturation_priors,)


@app.cell(hide_code=True)
def _(Prior, saturation_prior_params, saturation_priors):
    if saturation_prior_params.value is not None:
        updated_saturation_priors = {
            param_name: Prior.from_dict(
                {
                    "dist": saturation_priors[param_name].to_dict()["dist"],
                    "kwargs": param_vals,
                }
            )
            for param_name, param_vals in saturation_prior_params.value.items()
        }
    else:
        updated_saturation_priors = saturation_priors
    return (updated_saturation_priors,)


@app.cell(hide_code=True)
def _():
    import matplotlib.pyplot as plt

    return (plt,)


@app.cell(hide_code=True)
def _():
    from pymc_marketing.prior import Prior

    return (Prior,)


@app.cell(hide_code=True)
def _(
    SATURATION_TRANSFORMATIONS,
    saturation_selector,
    updated_saturation_priors,
):
    saturation = SATURATION_TRANSFORMATIONS[saturation_selector.value](
        priors=updated_saturation_priors
    )
    saturation_prior_samples = saturation.sample_prior(draws=1000)
    saturation_curve = saturation.sample_curve(saturation_prior_samples)
    return saturation, saturation_curve


if __name__ == "__main__":
    app.run()
