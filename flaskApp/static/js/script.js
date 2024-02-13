 $(document).ready(function(){
            $('#inputForm').submit(function(event) {
                event.preventDefault();
                var min_budget = $('#min-budget').val();
                var max_budget = $('#max-budget').val();
                var laptop_type = $('#type-dropdown').val();
                $.ajax({
                    type: 'POST',
                    url: '/result',
                    data: {
                        min_budget: min_budget,
                        max_budget: max_budget,
                        laptop_type: laptop_type
                    },
                    success: function(response) {
                      
                        // Remove the Laptop Cards available earlier
                        $('#main-content').empty();

                        laptops_list = response.data;

                        function createLaptopCard(product) {
                            var card = $('<div class="product-card">' +
                                         '<div class="product-image-container">' +
                                             '<a href="' + product[11] + '" target="_blank" title="' + product[1] + '">' +
                                                 '<img src="' + product[0] + '" class="product-image">' +
                                             '</a>' +
                                         '</div>' +
                                         '<div class="product-details">' +
                                             '<h6 class="product-name">' + product[1] + '</h6>' +
                                             '<p class="product-price">₹' + product[2] + '</p>' +
                                             '<p class="product-processor">' + product[3] + '</p>' +
                                             '<p class="product-ram">' + product[4] + '</p>' +
                                             '<p class="product-rom">' + product[5] + '</p>' +
                                             '<p class="product-graphics">' + product[6] + '</p>' +
                                             '<p class="product-display">' + product[7] + '</p>' +
                                             '<p class="refresh-rate">' + product[8] + '</p>' +
                                             '<p class="product-os">' + product[9] + '</p>' +
                                             '<p class="product-recommendation-score">' + product[10] + '%</p>' +
                                         '</div>' +
                                     '</div>');
                            $('#main-content').append(card);
                        }

                        // Append the laptop cards from the filtered_laptops list
                        for (var i = 0; i < laptops_list.length; i++) {
                            createLaptopCard(laptops_list[i]);
                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            });
        });