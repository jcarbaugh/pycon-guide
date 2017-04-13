import $ from 'jquery'
import 'reconnectingwebsocket'

$(document).ready(function() {

  $('.logo__link').on('click', function(e) {
    e.preventDefault();
    $('html, body').animate({scrollTop: '0'}, 300, 'swing');
  });

  $('.card').on('click', function(e) {
    $(this).toggleClass('is-flipped');
  });

  $('.card__link a').on('click', function(e) {
    e.stopPropagation();
  });

  if (window.wsSessionKey) {

    var proto = window.location.protocol == 'https:' ? 'wss' : 'ws';
    var host = window.location.host;
    var socket = new ReconnectingWebSocket(
      proto + '://' + host + '/presentations?session_key=' + wsSessionKey);

    socket.onmessage = function(e) {

      console.log(e.data);

      var messageParts = e.data.split(':');
      var action = messageParts[0];
      var presId = messageParts[1];
      var $card = $('.card[data-presentation-id=' + presId + ']');
      var $btn = $card.find('a.card-button');

      if (action === 'disinterested') {
        $btn.removeClass('is-selected');
        $btn.html('Add to Calendar');
        $btn.attr('data-selected', 'false');
        $card.removeClass('is-selected');
      } else {
        $btn.addClass('is-selected');
        $btn.html('Remove from Calendar');
        $btn.attr('data-selected', 'true');
        $card.addClass('is-selected');
      }
    };

    $('.js-select').on('click', function(e) {
      e.stopPropagation();

      var presId = $(this).data('presentation-id');
      var card = $(this).closest('.card');
      var $this = $(this);

      if ($this.attr('data-selected') === "true") {
        // $this.removeClass('is-selected');
        // $this.html('Add to Calendar');
        // $this.attr('data-selected', 'false');
        // card.removeClass('is-selected');
        socket.send("disinterested:" + presId);
      } else {
        // $this.addClass('is-selected');
        // $this.html('Remove from Calendar');
        // $this.attr('data-selected', 'true');
        // card.addClass('is-selected');
        socket.send("interested:" + presId);
      }
    });

  }

});
