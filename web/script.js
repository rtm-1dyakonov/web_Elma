
const displayNone = 'none';
const displayBlock = 'block';

const countIntent = 3;

const input = document.querySelector('.form__input');
const button = document.querySelector('.form__button');
const errorInput = document.querySelector('.error');
const answer = document.querySelector('.answer');
const bodyTable = document.querySelector('tbody');

const checkValueInput = () => {
    const valueInput = input.value;
    const regular = /^[а-яё\s-]+$/i;
    const countWord = valueInput.split(' ').length;

    errorInput.innerHTML = '';
    answer.style.display = displayNone;

    if (valueInput.length === 0) {
        errorInput.innerHTML = 'Пустая фраза, введите предложение в окно';
    } else if (countWord > 14) {
        errorInput.innerHTML = 'Предложение превышает 14 слов, введите заново';
    } else if (!regular.test(valueInput)) {
        errorInput.innerHTML = 'Предложение может состоять только из кириллицы, введите заново';
    } else {
        answer.style.display = displayBlock;
        createBodyTablet(valueInput);
    }
}

const createBodyTablet = (valueInput) => {
    bodyTable.innerHTML = '';

    let intents = [];
    let score = [];

    eel.intent(valueInput)((obj) => {
        obj.forEach(element => {
            intents.push(element);
        });
    });

    eel.score(valueInput)((obj) => {
        obj.forEach(element => {
            score.push(element);
        });
    });

    setTimeout(() => {
        for (let i = 0; i < countIntent; i++) {
            bodyTable.innerHTML += `
                <tr>
                    <td>${intents[i]}</td>
                    <td>${score[i]} %</td>
                </tr>
            `;
        }
    }, 2000);
}

button.addEventListener('click', () => {
    checkValueInput();
});