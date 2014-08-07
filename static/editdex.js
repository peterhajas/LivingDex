$('ul').click
(
    function (event)
    {
        clickedElement = event.target;
        toggledPokemon = clickedElement.id;
        console.log(toggledPokemon);
        console.log(event)
        $.post('/togglePokemon', {username : user, toggledPokemon : toggledPokemon});
        
        pokemonState = clickedElement.className;
        var newPokemonState = '';
        if(pokemonState == 'uncaught')
        {
            newPokemonState = 'caught';
        }
        else if(pokemonState = 'caught')
        {
            newPokemonState = 'uncaught';
        }
        console.log(pokemonState);

        clickedElement.className = newPokemonState;
    }
);
