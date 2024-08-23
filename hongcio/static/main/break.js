let isBrake = [
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false],
    [false, false, false, false, false]
];



function setBreak(period, day, value){
    if(period=='*'){
        value = !isBrake[0][day-1];
        for(var i=1; i<14+1; i++){
            setBreak(i, day, value);
        }
        return;
    }
    else if(day=='*'){
        value = !isBrake[period-1][0];
        for(var i=1; i<5+1; i++){
            setBreak(period, i, value);
        }
        return;
    }

    if(value==undefined){
        value = !isBrake[period-1][day-1];
    }

    isBrake[period-1][day-1] = value;

    var elem = document.querySelector(`#r${period}c${day}`);
    elem.classList.remove("checked");
    if(value) elem.classList.add("checked");

    setCookie("break", serialzieBreaks(isBrake), 30);
}


function serialzieBreaks(breaks){
    let result = "";
    for(let i=0; i<isBrake.length; i++){
        for(let j=0; j<isBrake[i].length; j++){
            if(breaks[i][j]) result += `r${i+1}l${j+1},`;
        }
    }
    return result.slice(0, -1);
}


function loadBreaks(){
    var breaks = getCookie("break");

    breaks = breaks.split(",");

    breaks.forEach(b => {
        var temp = b.split('l');
        var period = parseInt(temp[0].slice(1));
        var day = parseInt(temp[1]);
        setBreak(period, day, true);
    });
}

loadBreaks();