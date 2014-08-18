$('ul').click
(
    function (event)
    {
        var clickedElement = event.target;

        if(!$(clickedElement).hasClass('pokemonCell'))
        {
            while(true)
            {
                if($(clickedElement).hasClass('pokemonCell'))
                {
                    break;
                }
                var parentElement = clickedElement.parentNode;
                if(parentElement != null)
                {
                    clickedElement = parentElement;
                }
                else
                {
                    // No clicked pokemon here. Return.
                    return;
                }
            }
        }


        toggledPokemon = clickedElement.id;
        $.post('/togglePokemon', {username : user, toggledPokemon : toggledPokemon});

        $(clickedElement).toggleClass('uncaught');
        $(clickedElement).toggleClass('caught');

        updateProgressBar();
    }
);
