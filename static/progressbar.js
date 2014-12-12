function progressBarRGBAString(percentage)
{
    var unitPercentage = percentage / 100.0;
    var distanceFromHalf = 2 * Math.abs(Math.abs(unitPercentage) - 0.5);
    var nonFullComponent = 255 * distanceFromHalf;
    nonFullComponent = 255 - nonFullComponent;
    nonFullComponent = Math.round(nonFullComponent);
    var redComponent;
    var greenComponent;

    if (unitPercentage <= 0.5)
    {
        redComponent = 255;
        greenComponent = nonFullComponent;
    }
    else
    {
        greenComponent = 255;
        redComponent = nonFullComponent;
    }

    return 'rgba(' + redComponent + ',' + greenComponent + ',0,1)'
}

function updateProgressBar()
{
    var allPokemon = document.getElementsByClassName('valid').length;
    var capturedPokemon = document.getElementsByClassName('caught valid').length;

    var progressBarFilledElement = document.getElementsByClassName('filledBar')[0];
    var progressBarText = document.getElementsByClassName('progressBarText')[0];

    var percentComplete = capturedPokemon / allPokemon;
    percentComplete *= 100;

    var percentCompleteText = (percentComplete).toFixed(1) + '%';
    var percentCompleteFilledWidth = percentComplete + '%';
    var percentCompleteRGBA = progressBarRGBAString(percentComplete);

    progressBarText.innerHTML = percentCompleteText;
    progressBarFilledElement.style.width = percentCompleteFilledWidth;
    progressBarFilledElement.style.backgroundColor = percentCompleteRGBA;
}
