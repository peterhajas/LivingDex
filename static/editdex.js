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


        pokemon = clickedElement.id;

        var requestContents = {username : user, pokemon : pokemon};
        var requestURL = '/uncatchPokemon'

        if($(clickedElement).hasClass('uncaught'))
        {
            requestURL = '/catchPokemon'
        }

        $.post(requestURL, requestContents);

        $(clickedElement).toggleClass('uncaught');
        $(clickedElement).toggleClass('caught');

        updateProgressBar();
    }
);
