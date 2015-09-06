#include <pebble.h>
#include "main_window.h"
#include "success_window.h"
#include "crash_window.h"

static Window *main_window;
static Window *game_over_window;

enum {
  BUTTON_PRESS_KEY = (uint32_t) 0,
  LEFT_PRESS = (uint8_t) 1,
  RIGHT_PRESS = (uint8_t) 2,
  GAME_OVER = (uint32_t) 3,
  GAME_WIN = (uint8_t) 4,
  GAME_LOSS = (uint8_t) 5,
  RESET_PRESS = (uint8_t) 6,
  START_PRESS = (uint8_t) 7
};

static void send_simple_dict(uint32_t key, uint8_t val) {
  DictionaryIterator *iter;
  app_message_outbox_begin(&iter);

  if (iter == NULL)
    return;

  dict_write_uint8(iter, key, val);
  dict_write_end(iter);

  app_message_outbox_send();
}

static void up_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_simple_dict(BUTTON_PRESS_KEY, LEFT_PRESS);
}

static void down_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_simple_dict(BUTTON_PRESS_KEY, RIGHT_PRESS);
}

static void start_click_handler(ClickRecognizerRef recognizer, void *context) {
  send_simple_dict(BUTTON_PRESS_KEY, START_PRESS);
}

static void game_over_window_click_handler(ClickRecognizerRef recognizer, void *context) {
  vibes_cancel();
  window_stack_pop(true);
  send_simple_dict(BUTTON_PRESS_KEY, RESET_PRESS);
}

static void outbox_fail_callback(DictionaryIterator *iterator, AppMessageResult reason, void *context) {
  switch (reason) {
    case APP_MSG_SEND_TIMEOUT:
      APP_LOG(APP_LOG_LEVEL_ERROR, "APP_MSG_SEND_TIMEOUT");
      break;
    default:
      APP_LOG(APP_LOG_LEVEL_ERROR, "I have no idea");
  }
}

static void main_click_config_provider(void *context) {
  window_single_repeating_click_subscribe(BUTTON_ID_UP, (uint16_t) 100, up_click_handler);
  window_single_repeating_click_subscribe(BUTTON_ID_DOWN, (uint16_t) 100, down_click_handler);
  window_single_click_subscribe(BUTTON_ID_SELECT, start_click_handler);
}

static void game_over_click_config_provider(void *context) {
  window_single_click_subscribe(BUTTON_ID_UP, game_over_window_click_handler);
  window_single_click_subscribe(BUTTON_ID_DOWN, game_over_window_click_handler);
  window_single_click_subscribe(BUTTON_ID_SELECT, game_over_window_click_handler);
  window_single_click_subscribe(BUTTON_ID_BACK, game_over_window_click_handler);
}

static void game_over_handler(DictionaryIterator *iter, void *context) {
  app_log(APP_LOG_LEVEL_DEBUG, __FILE__, __LINE__, "Calling receive_handshake_cmd");

  Tuple *game_over_tuple = dict_find(iter, GAME_OVER);
  if (game_over_tuple->value->uint8 == GAME_WIN) {
    // Update screen for win status
    game_over_window = show_success_window();
    window_set_click_config_provider(game_over_window, game_over_click_config_provider);
  } else if (game_over_tuple->value->uint8 == GAME_LOSS) {
    // Update screen for loss status
    game_over_window = show_crash_window();
    window_set_click_config_provider(game_over_window, game_over_click_config_provider);
    vibes_long_pulse();
  }

  light_enable_interaction();
}

static void init(void) {
  // Open AppMessage to transfers
  app_message_open(app_message_inbox_size_maximum(), app_message_outbox_size_maximum());
  app_message_register_outbox_failed(outbox_fail_callback);
  app_message_register_inbox_received(game_over_handler);

  main_window = show_main_window();
  window_set_click_config_provider(main_window, main_click_config_provider);
}

static void deinit(void) {
  hide_main_window();
  window_destroy(game_over_window);
}

int main(void) {
  init();
  app_event_loop();
  deinit();
}
