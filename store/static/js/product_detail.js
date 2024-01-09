$(document).ready(function() {
    $('.add-to-cart-btn').on('click', function() {
      var form = $(this).closest('form');
      var data = {
        'product_id': form.find('input[name="product_id"]').val(),
        'color': form.find('select[name="color"] option:selected').val(),
        'size': form.find('input[name="size"]:checked').val(),
        'quantity': form.find('input[name="quantity"]').val(),
        'csrfmiddlewaretoken': '{{ csrf_token }}'
      };
      $.ajax({
        url: form.attr('action'),
        type: form.attr('method'),
        data: data,
        success: function(response) {
          console.log('Товар успешно добавлен в корзину.');
        },
        error: function(jqXHR, textStatus, errorThrown) {
          console.log('Ошибка при добавлении товара в корзину:', errorThrown);
        }
      });
      return false;
    });
  });