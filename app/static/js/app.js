/* global $ */

var FEED_REFRESH_INTERVAL_MS = 1000
// window.MINISOCIAL defined in the view
var FEED_REFRESH_URL = window.MINISOCIAL.FEED_REFRESH_URL
var INITIAL_STATE = window.MINISOCIAL.INITIAL_STATE
var LAST_STATE = window.MINISOCIAL.LAST_STATE
var MESSAGE_ENDPOINT = window.MINISOCIAL.MESSAGE_ENDPOINT

$(function () {
  // Populate with initial state

  INITIAL_STATE.forEach(addMessageToView)

  // Setup CSRF

  $.ajaxSetup({
    beforeSend: function (xhr) {
      if (!this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
      }
    }
  })

  // Handle message sending

  $('#form_post_message').on('submit', function onSubmit (e) {
    e.preventDefault()

    var submitButton = $(this).find('input[type=submit]')
    var messageInput = $(this).find('input[name=message]')
    var formUrl = $(this).attr('action')
    var formMethod = $(this).attr('method')

    $(submitButton).attr('disabled', 'disabled')

    $.ajax({
      url: formUrl,
      type: formMethod,
      data: { message: messageInput.val() }
    }).done(function (data) {
      $(messageInput).val('')
    }).always(function () {
      $(submitButton).removeAttr('disabled')
    })
  })

  // Handle message deletion

  $('body').on('click', '.delete', function onDelete (e) {
    e.preventDefault()

    var messageId = $(this).closest('.message').attr('data-id')

    $.ajax({
      url: MESSAGE_ENDPOINT + messageId + '/',
      type: 'DELETE'
    }).done(function (data) {
      deleteMessageFromView(messageId)
    })
  })

  // Handle feed refreshing

  var lastState = LAST_STATE
  var feedRefreshTimeout
  var armFeedRefresh = function () {
    if (feedRefreshTimeout) clearTimeout(feedRefreshTimeout)

    feedRefreshTimeout = setTimeout(function handleFeedRefresh () {
      $.get(FEED_REFRESH_URL, { last_state: lastState }).done(function (data) {
        if (data.last_state > lastState) {
          handleFeedToView(data.feed)
          lastState = data.last_state
        }
      }).always(function () {
        armFeedRefresh()
      })
    }, FEED_REFRESH_INTERVAL_MS)
  }

  armFeedRefresh()

  // Functions

  function deleteMessageFromView (id) {
    $('ul[data-id=' + id + ']').remove()
  }

  function addMessageToView (entry) {
    var messageHtml = ''
    messageHtml += '<ul data-id="' + entry.id + '" class="message">'
    messageHtml += '  <li class="username">' + entry.username + ' (<span class="date">' + formatDate(new Date(entry.pub_date)) + '</span>)</li>'
    messageHtml += '  <li class="text">' + escapeHtml(entry.message_text) + '</li>'
    if (entry.mine) messageHtml += '  <li><button class="delete">Supprimer</button></li>'
    messageHtml += '</ul>'

    var messageEl = $(messageHtml)

    $('.messages').prepend(messageEl)
  }

  function handleFeedToView (feed) {
    feed.forEach(function (entry) {
      var isAddition = entry.type === '+'

      if (isAddition) addMessageToView(entry)
      else deleteMessageFromView(entry.id)
    })
  }
})

// Helpers

function getCookie (name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = $.trim(cookies[i])
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

function escapeHtml (value) {
  return $('<div/>').text(value).html()
}

function formatDate (date) {
  function pad (n) { return n < 10 ? '0' + n : n }

  return date.getDate() + '/' +
    pad(date.getMonth() + 1) + '/' +
    pad(date.getFullYear()) + ' ' +
    pad(date.getHours()) + ':' +
    pad(date.getMinutes()) + ':' +
    pad(date.getSeconds())
}
