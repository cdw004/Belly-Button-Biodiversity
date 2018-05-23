function getSampleNames(){
    var selector = document.getElementById('selDataset');
    var url = "/names";
    Plotly.d3.json(url, function(error, response) {
        if (error) return console.warn(error);
        var data = response;
        data.map(function(sample){
            var option = document.createElement('option')
            option.text = sample
            option.value = sample
            selector.appendChild(option)
        });
    });
};

getSampleNames();

function optionChanged(sample){
    updatePie(sample);
    updateBubble(sample);
    updateMetadata(sample);
};
