$(document).ready(function() {
    // Обработчик событий для поля количества
    $('.quantity-input').on('input', function() {
      var form = $(this).closest('form');
      var data = {
        'product_id': form.find('input[name="product_id"]').val(),
        'action': 'update',
        'quantity': $(this).val(),
        'color': form.find('select[name="color"] option:selected').val(),
        'size': form.find('input[name="size"]:checked').val()
      };
      $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: data,
        success: function(response) {
          // Обновление стоимости и общей стоимости в таблице
          var row = $(response).find('tr[data-item-id="' + form.data('item-id') + '"]');
          var price = row.find('.price').text();
          var total = row.find('.total-price').text();
          form.closest('tr').find('.price').html(price);
          form.closest('tr').find('.total-price').html(total);
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log('Ошибка при отправке формы:', errorThrown);
        }
      });
    });
  });