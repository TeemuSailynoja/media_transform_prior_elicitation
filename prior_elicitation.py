# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "matplotlib==3.10.3",
#     "pymc-marketing==0.15.0",
# ]
# ///

import marimo

__generated_with = "0.14.10"
app = marimo.App(width="columns")


@app.cell(column=0, hide_code=True)
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
    saturation_prior_samples = saturation.sample_prior(draws=2000)
    saturation_curve = saturation.sample_curve(saturation_prior_samples)
    return saturation, saturation_curve


@app.cell(column=1, hide_code=True)
def _(plt, saturation_priors, updated_saturation_priors):
    _fig = plt.figure(figsize=(9, 4))

    for idx, (param_name, prior) in enumerate(updated_saturation_priors.items()):
        _ax = plt.subplot(1, len(updated_saturation_priors.keys()), idx + 1)
        _ax = saturation_priors[param_name].preliz.plot_pdf(
            ax=_ax, legend=None, color="grey"
        )
        _ax = prior.preliz.plot_pdf(ax=_ax, legend="title")
        # _ax.set_title(param_name)
        # _ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    _ax
    return


@app.cell(hide_code=True)
def _(saturation, saturation_curve):
    _fig, _ax = saturation.plot_curve_hdi(saturation_curve)
    _fig, _ax = saturation.plot_curve_hdi(
        saturation_curve, hdi_kwargs={"hdi_prob": 0.5}, axes=_ax
    )
    _fig, _ax = saturation.plot_curve(saturation_curve, axes=_ax)
    _ax[0]
    return


@app.cell
def _():
    return


@app.cell(column=2)
def _(ADSTOCK_TRANSFORMATIONS, mo):
    adstock_selector = mo.ui.dropdown(
        label="Select adstock function:",
        options=ADSTOCK_TRANSFORMATIONS.keys(),
        value="no_adstock",
    )
    adstock_selector
    return (adstock_selector,)


@app.cell
def _(adstock_priors, mo):
    adstock_prior_params = mo.ui.dictionary(
        label="adstock function priors",
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
            for param, param_prior in adstock_priors.items()
        },
    ).form()
    adstock_prior_params
    return (adstock_prior_params,)


@app.cell
def _(default_adstock):
    adstock_priors = default_adstock.function_priors
    return (adstock_priors,)


@app.cell
def _(Prior, adstock_prior_params, adstock_priors):
    if adstock_prior_params.value is not None:
        updated_adstock_priors = {
            param_name: Prior.from_dict(
                {
                    "dist": adstock_priors[param_name].to_dict()["dist"],
                    "kwargs": param_vals,
                }
            )
            for param_name, param_vals in adstock_prior_params.value.items()
        }
    else:
        updated_adstock_priors = adstock_priors
    return (updated_adstock_priors,)


@app.cell(hide_code=True)
def _():
    from pymc_marketing.mmm.components.adstock import ADSTOCK_TRANSFORMATIONS

    return (ADSTOCK_TRANSFORMATIONS,)


@app.cell
def _(ADSTOCK_TRANSFORMATIONS, adstock_selector):
    default_adstock = ADSTOCK_TRANSFORMATIONS[adstock_selector.value](l_max=12)
    return (default_adstock,)


@app.cell
def _(ADSTOCK_TRANSFORMATIONS, adstock_selector, updated_adstock_priors):
    adstock = ADSTOCK_TRANSFORMATIONS[adstock_selector.value](
        priors=updated_adstock_priors, l_max=12
    )
    adstock_prior_samples = adstock.sample_prior(draws=1000)
    adstock_curve = adstock.sample_curve(adstock_prior_samples)
    return adstock, adstock_curve


@app.cell(column=3)
def _(adstock_priors, plt, updated_adstock_priors):
    _fig = plt.figure(figsize=(9, 4))

    for _idx, (_param_name, _prior) in enumerate(updated_adstock_priors.items()):
        _ax = plt.subplot(1, len(updated_adstock_priors.keys()), _idx + 1)
        _ax = adstock_priors[_param_name].preliz.plot_pdf(
            ax=_ax, legend=None, color="grey"
        )
        _ax = _prior.preliz.plot_pdf(ax=_ax, legend="title")
        # _ax.set_title(param_name)
        # _ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5)
    _ax
    return


@app.cell
def _(adstock, adstock_curve):
    _fig, _ax = adstock.plot_curve_hdi(adstock_curve)
    _fig, _ax = adstock.plot_curve_hdi(
        adstock_curve, hdi_kwargs={"hdi_prob": 0.5}, axes=_ax
    )
    _fig, _ax = adstock.plot_curve(adstock_curve, axes=_ax)
    _ax[0]
    return


if __name__ == "__main__":
    app.run()
