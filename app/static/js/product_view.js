const countInput = $("#count_input")
const countDowntext = $("#count_input_downtext")
const submitBtn = $("#submit_btn")
const total = $("#total")

function inputWrong(el) {
    el.removeClass('is-valid')
    el.addClass('is-invalid')
}

function inputCorrect(el) {
    el.addClass('is-valid')
    el.removeClass('is-invalid')
}

function update() {
    const count = +countInput.val()
    const cost = count * price
    const canSubmit = count <= maxCount && 0 < count && cost <= currentBill

    submitBtn.prop('disabled', !canSubmit)

    if (!canSubmit) {
        total.text('0')
        inputWrong(countInput)
        if (count > maxCount) {
            countDowntext.text('Число превышает количество товаров, выставленных на продажу')
        } else if (count <= 0) {
            countDowntext.text('Число должно быть больше 0')
        } else if (cost > currentBill) {
            countDowntext.text('У вас нет столько денег')
            total.text(cost)
        }
    } else {
        total.text(cost)
        countDowntext.text('')
        inputCorrect(countInput)
    }
}

countInput.on('input', update)
