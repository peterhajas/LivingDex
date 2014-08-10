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
                var parent = $(clickedElement).parent();
                if(parent != null)
                {
                    clickedElement = parent;
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
    }
);
