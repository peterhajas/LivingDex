function arrayCount(array) // what
{
    var count = array.filter(function(value) { return value !== undefined }).length;
    return count;
}

function updateDisplayForDex(dexName)
{
    var allDexItems = document.getElementsByClassName('dexPickerDexTitle');

    for(var i = 0; i < allDexItems.length; i++)
    {
        var dexItem = allDexItems[i];
        $(dexItem).removeClass('selected');
    }

    var selectedDexElement = document.getElementById(dexName);

    $(selectedDexElement).addClass('selected');

    var pokemonInDex = dexes[dexName];

    var allPokemon = document.getElementsByClassName('pokemonCell');

    for(var i = 0; i < allPokemon.length; i++)
    {
        var pokemonElement = allPokemon[i];
        var pokemonNumber = pokemonElement.id;
        var pokemonNumber = Math.round(pokemonNumber);

        if(pokemonInDex.indexOf(pokemonNumber) == -1)
        {
            $(pokemonElement).removeClass('valid');
            $(pokemonElement).addClass('invalid');
        }
        else
        {
            $(pokemonElement).removeClass('invalid');
            $(pokemonElement).addClass('valid');
        }
    }

    updateProgressBar();
}

function populateDexPicker()
{
    var dexNames = Object.keys(dexes);
    var numberOfDexes = arrayCount(dexNames);

    for(var i = 0; i < numberOfDexes; i++)
    {
        var dexName = dexNames[i];
        console.log(dexName);

        var dexPickerContainerElement = document.getElementsByClassName('dexPicker')[0];
        var dexPickerDexTitleElement = document.createElement('div');
        dexPickerDexTitleElement.innerHTML = dexName;
        dexPickerDexTitleElement.className = 'dexPickerDexTitle';

        $(dexPickerDexTitleElement).click(function() {
            updateDisplayForDex(this.innerHTML);
        });

        dexPickerDexTitleElement.id = dexName;
        dexPickerContainerElement.appendChild(dexPickerDexTitleElement);
    }
}

