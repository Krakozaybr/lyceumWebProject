const priceField = $("#price_input")
const countField = $("#count_input")
const descriptionField = $("#description_input")
const total = $("#total")
const submitBtn = $("#submit")
const countInputDowntext = $("#count_input_downtext")
const priceInputDowntext = $("#price_input_downtext")

function update() {
    const count = +countField.val()
    const price = +priceField.val()
    const canSubmit = (
        count <= maxCount
        && count > 0
        && price > 0
        && descriptionField.val().replace(' ', '') !== ''
    )

    submitBtn.prop('disabled', !canSubmit)

    if (!canSubmit) {
        total.text('0')
    } else {
        total.text(count * price + '')
    }
}

function updateCountField() {
    const count = +countField.val()
    if (count <= 0) {
        countField.removeClass('is-valid')
        countField.addClass('is-invalid')
        countInputDowntext.text('Значение должно быть больше 0')
    } else if (count > maxCount) {
        countField.removeClass('is-valid')
        countField.addClass('is-invalid')
        countInputDowntext.text('У вас нет столько свободных предметов. Максимум: ' + maxCount)
    } else {
        countField.addClass('is-valid')
        countField.removeClass('is-invalid')
        countInputDowntext.text('')
    }
    update()
}

function updatePriceField() {
    const count = +priceField.val()
    if (count <= 0) {
        priceField.removeClass('is-valid')
        priceField.addClass('is-invalid')
        priceInputDowntext.text('Значение должно быть больше 0')
    } else if (count > 10 ** 10) {
        priceField.removeClass('is-valid')
        priceField.addClass('is-invalid')
        priceInputDowntext.text('Значение слишком большое')
    } else {
        priceField.addClass('is-valid')
        priceField.removeClass('is-invalid')
        priceInputDowntext.text('')
    }
    update()
}

countField.on('input', updateCountField)
priceField.on('input', updatePriceField)
descriptionField.on('input', update)

update()
