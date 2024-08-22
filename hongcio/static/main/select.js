const trashSvgPath = document.querySelector("#trash").innerHTML;

const primaryContainer = document.querySelector(".primary");
const nonPrimaryContainer = document.querySelector(".non-primary");

const form = document.querySelector(".lecture-select-form");

const courseNumberField = form.querySelector("input[name='course-name']");
const primaryField = form.querySelector("input[name='is-primary']");


let selectedPrimaryLectures = [];
let selectedNonPrimaryLectures = [];


function selectLecture(){
    var courseNumber = courseNumberField.value;
    var isPrimary = primaryField.checked;

    courseNumberField.value = "";

    
    if(courseNumber==""){
        alert("학수번호를 입력해주세요!");
        return;
    }

    courseNumber = courseNumber.split("-")[0];

    if(isNaN(courseNumber)){
        alert("올바른 학수번호를 입력해 주세요!");
        return;
    }
    
    if(selectedPrimaryLectures.includes(courseNumber) || selectedNonPrimaryLectures.includes(courseNumber)){
        alert("이미 추가한 과목이에요!");
        return;
    }

    getLecture(courseNumber, isPrimary);
}


function getLecture(courseNumber, isPrimary) {
    url = "/lecture";
    url += "?course-number=" + courseNumber;
    fetch(url)
        .then((res) => {
            if (res.ok) return res.json();

            else if (res.status == 404) {
                console.log(res)
                alert("강의를 검색할 수 없습니다.");
                throw new Error(404);
            }
        })
        .then((data) => {
            console.log(data);
            var elem = generateLectureHtml(data.courseNumber, data.name, data.department, data.classification);
            if (isPrimary) {
                selectedPrimaryLectures.push(data.courseNumber);
                primaryContainer.appendChild(elem);
            }
            else {
                selectedNonPrimaryLectures.push(data.courseNumber);
                nonPrimaryContainer.appendChild(elem);
            }
            saveSelectedLectures();
        })
        .catch((error) => {
            console.log(error);
        });
}

function generateLectureHtml(courseNumber, name, department, classification){
    var elem = document.createElement('div');
    elem.id = `l${courseNumber}`;
    elem.classList.add('lecture');
    elem.innerHTML = `
    <span class="lecture-wrapper">
        <span class="course-name">${courseNumber}</span>
        <span class="name">${name}</span>
    </span>
    <span class="lecture-wrapper">
        <span class="department">${department}</span>
        <span class="classification">${classification}</span>
        <button onclick="deleteLecture('${courseNumber}');">
            <img src="${trashSvgPath}" alt="X">
        </button>
    </span>`;
    return elem;
}


function deleteLecture(courseNumber){
    selectedPrimaryLectures = selectedPrimaryLectures.filter((e) => e!=courseNumber);
    selectedNonPrimaryLectures = selectedNonPrimaryLectures.filter((e) => e!=courseNumber);
    document.querySelector(`#l${courseNumber}`).remove();
    saveSelectedLectures();
}


function setCookie(name, value, exp) {
    var date = new Date();
    date.setTime(date.getTime() + exp * 24 * 60 * 60 * 1000); 
    document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
}

function getCookie(name){
    var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
    return value? value[2] : null;
};


function saveSelectedLectures(){
    setCookie('primary', selectedPrimaryLectures.toString(), 30);
    setCookie('nonPrimary', selectedNonPrimaryLectures.toString(), 30);
}


function loadSelectedLectures(){
    var primaryLectures = getCookie('primary');
    var nonPrimaryLectures = getCookie('nonPrimary');

    primaryLectures = primaryLectures.split(",");
    nonPrimaryLectures = nonPrimaryLectures.split(",");

    primaryLectures.forEach(courseNumber => {
        console.log(courseNumber)
        if(courseNumber!="") getLecture(courseNumber, true);
    });
    nonPrimaryLectures.forEach(courseNumber => {
        console.log(courseNumber)
        if(courseNumber!="") getLecture(courseNumber, false);
    });
}
loadSelectedLectures();