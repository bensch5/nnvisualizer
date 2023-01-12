import raylib as rl
from pyray import *
import json

# configuration
DISTANCE_X, DISTANCE_Y = 400, 200  # distances inbetween neurons
MULT_CONN = 10  # factor by which line thickness for connections is multiplied
RADIUS = 50  # size/radius of each neuron
FONT_SIZE = 16  # font size


def main():
    # read input file
    with open("input.json") as file:
        data = json.load(file)

    # add all layers to a list (to simplify iteration later on)
    layers = [data["InputLayer"]]
    for hidden in data["HiddenLayer"]:
        layers.append(hidden)
    layers.append(data["OutputLayer"])

    # determine size of the biggest layer (used to center smaller layers properly)
    max_layer = 0
    for layer in layers:
        neurons = layer["NeuronList"]
        max_layer = max(max_layer, len(neurons))

    # window settings
    init_window(1600, 900, "NN Visualizer")
    set_target_fps(0)

    while not window_should_close():
        begin_drawing()
        clear_background(BLACK)

        # draw connections for entire network
        for x, layer in enumerate(layers):
            neurons = layer["NeuronList"]
            neuron_count = len(neurons)
            for y, neuron in enumerate(neurons):
                connected_list = neuron["ConnectedNeurons"]
                connected_count = len(connected_list)
                # draw connections to neurons in previous layer
                for y_prev, connected in enumerate(connected_list):
                    # figure out starting position for current connection
                    pos_x = 100 + RADIUS + DISTANCE_X * (x - 1)
                    # last part of sum: center connections according to the biggest layer
                    pos_y = 100 + RADIUS + (DISTANCE_Y * y_prev) + ((max_layer - connected_count) / 2) * DISTANCE_Y
                    start = Vector2(pos_x, pos_y)

                    # figure out ending position for current connection
                    pos_x = 100 + RADIUS + DISTANCE_X * x
                    # last part of sum: center connections according to the biggest layer
                    pos_y = 100 + RADIUS + (DISTANCE_Y * y) + ((max_layer - neuron_count) / 2) * DISTANCE_Y
                    end = Vector2(pos_x, pos_y)

                    # display negative values in red and positive values in blue
                    # and calculate line thickness from connection weight
                    weight = connected["Weight"]
                    if weight < 0:
                        thick = weight * -1 * MULT_CONN
                        color = RED
                    else:
                        thick = weight * MULT_CONN
                        color = SKYBLUE

                    # actually draw line
                    rl.DrawLineEx(start, end, thick, color)

        # draw neurons for entire network
        for x, layer in enumerate(layers):
            neurons = layer["NeuronList"]
            neuron_count = len(neurons)
            # draw neurons in current layer
            for y, neuron in enumerate(neurons):
                # figure out position for current neuron
                pos_x = 100 + RADIUS + DISTANCE_X * x
                # last part of sum: center neurons according to the biggest layer
                pos_y = 100 + RADIUS + (DISTANCE_Y * y) + ((max_layer - neuron_count) / 2) * DISTANCE_Y
                center = Vector2(pos_x, pos_y)

                # draw neuron
                rl.DrawCircleV(center, RADIUS, WHITE)
                rl.DrawCircleV(center, 0.9 * RADIUS, BLACK)

                # draw text below current neuron
                bias = neuron["Bias"]
                value = neuron["Value"]
                rl.DrawText(str.encode("Value: {}\nBias: {}".format(round(value, 3), round(bias, 3))),
                            int(pos_x - RADIUS), int(pos_y + RADIUS + 10), FONT_SIZE, WHITE)
        end_drawing()
    close_window()


if __name__ == '__main__':
    main()
