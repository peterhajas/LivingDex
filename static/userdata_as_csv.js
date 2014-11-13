function prepareCSVLink()
{
    var pokemonCells = document.getElementsByClassName('pokemonCell');

    var csvString = 'Number, Name, Caught\n'

    for(var i = 0; i < pokemonCells.length; i++)
    {
        var pokemonCell = pokemonCells[i];
        var number = pokemonCell.getElementsByClassName("pokemonCellNumber")[0].innerHTML;
        var name = pokemonCell.getElementsByClassName("pokemonCellName")[0].innerHTML;
        var caughtState = pokemonCell.className.split(/\s+/)[1];

        csvString+=number;
        csvString+=', ';
        csvString+=name;
        csvString+=', ';
        csvString+=caughtState;
        csvString+='\n';

        break;
    }

    var downloadLink = document.createElement("a");
    var csvURI = 'data:text/csv;charset=utf-8,' + csvString;
    downloadLink.href = csvString;
    downloadLink.download = 'dex.csv';
    downloadLink.innerHTML = "Download as CSV (experimental)";
    
    var container = document.getElementsByClassName("csvDownloadLinkContainer")[0];
    container.appendChild(downloadLink);
}
