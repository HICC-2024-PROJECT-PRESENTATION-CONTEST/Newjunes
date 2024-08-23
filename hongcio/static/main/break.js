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
    if(breaks==undefined || breaks=="") return;

    breaks = breaks.split(",");

    breaks.forEach(b => {
        var temp = b.split('l');
        var period = parseInt(temp[0].slice(1));
        var day = parseInt(temp[1]);
        setBreak(period, day, true);
    });
}

loadBreaks();


function generateSchedule(){
    var form = document.createElement("form");
    var param = new Array();
    var input = new Array();

    form.action = "https://newjunes.skybro2004.com/generate";
    form.method = "POST";

    breaks = getCookie('break');
    if(breaks!=""){
        breaks = breaks.split(',');
        for(var i=0; i<breaks.length; i++){
            breaks[i] = breaks[i].slice(1).split("l");
            breaks[i][0] = parseInt(breaks[i][0]) - 1
            breaks[i][1] = parseInt(breaks[i][1]) - 1
        }
    }
    
    param.push(['primary', JSON.stringify(getCookie('primary').split(','))]);
    param.push(['nonPrimary', JSON.stringify(getCookie('nonPrimary').split(','))]);
    // param.push(['break', JSON.stringify(getCookie('break').split(','))]);
    param.push(['break', JSON.stringify(breaks)]);


    for (var i = 0; i < param.length; i++) {
        input[i] = document.createElement("input");
        input[i].setAttribute("type", "hidden");
        input[i].setAttribute('name', param[i][0]);
        input[i].setAttribute("value", param[i][1]);
        form.appendChild(input[i]);
    }
    document.body.appendChild(form);
    form.submit();
    // console.log(param)
    // console.log(input)
}