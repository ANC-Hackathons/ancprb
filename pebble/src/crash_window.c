#include <pebble.h>
#include "crash_window.h"

// BEGIN AUTO-GENERATED UI CODE; DO NOT MODIFY
static Window *s_window;
static GFont s_res_gothic_24;
static GFont s_res_gothic_24_bold;
static GFont s_res_gothic_18;

static TextLayer *s_textlayer_1;
static TextLayer *s_textlayer_2;
static TextLayer *s_textlayer_3;

static Layer *s_canvas_layer_1;
static GBitmap *s_toaster_bitmap;

static void layer_update_proc(Layer *layer, GContext *ctx) {
  graphics_context_set_compositing_mode(ctx, GCompOpSet);
  graphics_draw_bitmap_in_rect(ctx, s_toaster_bitmap, gbitmap_get_bounds(s_toaster_bitmap));
}

static void initialise_ui(void) {
  s_window = window_create();
  Layer *window_layer = window_get_root_layer(s_window);
  #ifndef PBL_SDK_3
    window_set_fullscreen(s_window, 0);
  #endif

  window_set_background_color(s_window, GColorRed);
  s_res_gothic_24 = fonts_get_system_font(FONT_KEY_GOTHIC_24);
  s_res_gothic_24_bold = fonts_get_system_font(FONT_KEY_GOTHIC_24_BOLD);
  s_res_gothic_18 = fonts_get_system_font(FONT_KEY_GOTHIC_18);

  // s_textlayer_1
  s_textlayer_1 = text_layer_create(GRect(0, 0, 144, 30));
  text_layer_set_background_color(s_textlayer_1, GColorClear);
  text_layer_set_text(s_textlayer_1, "Sorry!");
  text_layer_set_text_alignment(s_textlayer_1, GTextAlignmentCenter);
  text_layer_set_font(s_textlayer_1, s_res_gothic_24_bold);
  layer_add_child(window_get_root_layer(s_window), (Layer *)s_textlayer_1);

  // s_textlayer_2
  s_textlayer_2 = text_layer_create(GRect(0, 25, 144, 70));
  text_layer_set_background_color(s_textlayer_2, GColorClear);
  text_layer_set_text(s_textlayer_2, "You crashed your toaster!");
  text_layer_set_text_alignment(s_textlayer_2, GTextAlignmentCenter);
  text_layer_set_font(s_textlayer_2, s_res_gothic_24);
  layer_add_child(window_get_root_layer(s_window), (Layer *)s_textlayer_2);

  // s_textlayer_3
  s_textlayer_3 = text_layer_create(GRect(0, 80, 144, 90));
  text_layer_set_background_color(s_textlayer_3, GColorClear);
  text_layer_set_text(s_textlayer_3, "Press any key to reset");
  text_layer_set_text_alignment(s_textlayer_3, GTextAlignmentCenter);
  text_layer_set_font(s_textlayer_3, s_res_gothic_18);
  layer_add_child(window_get_root_layer(s_window), (Layer *)s_textlayer_3);

  // Create canvas Layer
  s_toaster_bitmap = gbitmap_create_with_resource(RESOURCE_ID_TOASTER);
  s_canvas_layer_1 = layer_create(GRect(40, 105, 144, 168));
  layer_set_update_proc(s_canvas_layer_1, layer_update_proc);
  layer_add_child(window_layer, s_canvas_layer_1);
}

static void destroy_ui(void) {
  window_destroy(s_window);
  text_layer_destroy(s_textlayer_1);
  text_layer_destroy(s_textlayer_2);
  text_layer_destroy(s_textlayer_3);
  layer_destroy(s_canvas_layer_1);
}
// END AUTO-GENERATED UI CODE

static void handle_window_unload(Window* window) {
  destroy_ui();
}

Window* show_crash_window(void) {
  initialise_ui();
  window_set_window_handlers(s_window, (WindowHandlers) {
    .unload = handle_window_unload,
  });
  window_stack_push(s_window, true);
  APP_LOG(APP_LOG_LEVEL_DEBUG, "Done initializing, pushed window: %p", s_window);

  return s_window;
}

void hide_crash_window(void) {
  window_stack_remove(s_window, true);
}
