**Needed material.**

*   A <g class="gr_ gr_9 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="9" data-gr-id="9">raspberryPi</g> 3 or 3+ with adequate 2.5A or 3A power supply
*   Adafruit raspberryPi LED Bonnet ([<g class="gr_ gr_12 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling" id="12" data-gr-id="12">adafruit</g> link](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/pinouts))
*   6x of 64x64 LED panels ([<g class="gr_ gr_13 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling" id="13" data-gr-id="13">aliexpress</g> link](https://www.aliexpress.com/item/Lowest-price-HD-indoor-p2-led-matrix-module-rgb-full-color-hub75-meeting-room-exhibition-led/32855362755.html?spm=a2g0s.9042311.0.0.2f904c4dHzs5Gd))
*   Entire 3D printed structure ([<g class="gr_ gr_10 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="10" data-gr-id="10">onshape</g> link](https://cad.onshape.com/documents/914f60e8de4505754637efa6/w/804bacbd8ed48cb144be61ba/e/f97159b07fc228720e815eb4))
*   24x M3x10 socket button hex screws ([amazon link](https://www.amazon.co.uk/gp/product/B008RLY23U/ref=oh_aui_search_asin_title?ie=UTF8&psc=1))
*   A <g class="gr_ gr_11 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="11" data-gr-id="11">raspberryPI</g> camera
*   A longer ribbon for the camera ([<g class="gr_ gr_14 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling" id="14" data-gr-id="14">aliexpress</g> link](https://www.aliexpress.com/item/15Pin-Ribbon-Flex-CSI-Cable-with-15cm-30cm-50cm-100cm-200cm-Length-for-Raspberry-Pi/32889005025.html?spm=a2g0s.9042311.0.0.2f904c4dHzs5Gd))

**Software.**

The easiest way to get the setup running is by burning an image of the SD card (available here but now quite yet). The OS is (as usual) arch-<g class="gr_ gr_5 gr-alert gr_spell gr_inline_cards gr_run_anim ContextualSpelling ins-del multiReplace" id="5" data-gr-id="5">linux</g>. The library used to drive the LED is:

*   [hzeller](https://github.com/hzeller)/**[rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix)[](https://github.com/BNNorman/rpi-rgb-led-matrix-animator)**

**Assembly.**

![Schematics of assembly](https://labbook.gilest.ro/wp-content/uploads/2019/03/image.png)


*   Download and burn the PI image with the custo software (link)
*   Mount the 6 panels in a structure using the hex screws and the 3D printed parts.
*   If using 64x64 LED panels, the bonnet must first be modified to properly drive this configuration by soldiering a jumper on the back (see figure below).
*   Connect the bonnet to the PI and connect all the cables

![Modifications on the bonnet](https://cdn-learn.adafruit.com/assets/assets/000/063/007/medium640/led_matrices_addr-e-pad-bonnet.jpg?1538677462)

**The software.**

The software driving the buridan can be found here.
