function updateChests() {
    $(".chest-price").each(function () {
        if (current_bill < +$(this).data('price')) {
            $(this).removeClass('alert-success')
            $(this).addClass('alert-danger')
        } else {
            $(this).addClass('alert-success')
            $(this).removeClass('alert-danger')
        }
    })
    $('.chest-open').each(function () {
        $(this).prop('disabled', current_bill < +$(this).data('price'))
    })
}

function update(){
    updateChests()
    $('#balance').text(current_bill)
}

$(".chest-open").on("click", function () {
    const chest_id = +$(this).data('chest-id')
    console.log(chest_id)
    $.ajax({
        url: '/api/buy',
        method: 'POST',
        dataType: "json",
        contentType: 'application/json',
        data: JSON.stringify({
            'chest_id': chest_id
        }),
        success: data => {
            current_bill = data['bill']

            window.location.href = data['transaction']

            update()
        }, error: function (arg1, arg2) {
            alert(arg1.statusText)
        }
    })
})

update()
