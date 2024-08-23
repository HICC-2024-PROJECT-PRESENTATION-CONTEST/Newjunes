const lectures = JSON.parse(document.querySelector("#lectures").innerHTML.replace(/'/gi, '"'));
const result = JSON.parse(document.querySelector("#result").innerHTML.replace(/'/gi, '"'));

let caseNumber = 0;

const origin = document.querySelector("table").innerHTML;

function drawCase(caseNumber){
    document.querySelector("table").innerHTML = origin;
    
    var caseObj = result[caseNumber];

    var colorIndex = 0;
    caseObj.forEach(lecture => {
        var courseNumber = lecture[0];
        var divisionNumber = lecture[1];

        var periods = lectures[courseNumber]["division"][divisionNumber]["period"];

        
        periods.forEach(period => {
            var day = ["MON", "TUE", "WED", "THU", "FRI"].indexOf(period["day"]) + 1;
            var start = parseInt(period["start"]);
            var hour = parseInt(period["hour"]);

            var elem = document.querySelector(`#r${start}c${day}`);
            elem.rowSpan = hour;

            for(var temp=start+1; temp<start+hour; temp++){
                var tempElem = document.querySelector(`#r${temp}c${day}`);
                tempElem.remove();
            }

            elem.innerHTML = `<div>${lectures[courseNumber]["name"]}</div>`;
            elem.style.background = ["#d53e4f", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#e6f598", "#abdda4", "#66c2a5", "#3288bd"][colorIndex];
        });
        colorIndex++;
    });
}

const lectureWrapper = document.querySelector('.lecture-wrapper')
function setInfo(caseNumber){
    lectureWrapper.innerHTML = "";

    var caseObj = result[caseNumber];
    caseObj.forEach(lecture => {
        lectureWrapper.innerHTML += `
        <div class="lecture">
            <p class="course-number">${lecture[0]}-${lecture[1]}</p>
            <p class="name">${lectures[lecture[0]]["name"]}</p>
            <p class="professor">${lectures[lecture[0]]["division"][lecture[1]]["professor"]}</p>
        </div>
        `
    })

}

drawCase(caseNumber)
setInfo(caseNumber)

function setCase(caseN){
    if(caseN<0){
        caseNumber = 0;
        return;
    }
    if(result.length<=caseN){
        caseNumber = result.length - 1;
        return;
    }

    drawCase(caseNumber);
    setInfo(caseNumber);
}