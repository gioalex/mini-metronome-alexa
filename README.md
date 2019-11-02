Mini Metronome
==============

![logo](./mini_metronome.png)

Mini Metronome is a simple Alexa skill to provide a quick and easy metronome for musical instrument practice anywhere you have an Alexa enabled device.

This repo contains the code used for the lambda function which handles interactions from the skill model. It parses the user's intent and responds with an appropriate metronome from [Metronomer](https://metronomer.com).

## Development

To create a Lambda deployment package:

```
pip install -r requirements.txt -t skill_env
cp -r mini_metronome/ skill_env/
cd skill_env
zip -r ../mini-metronome.zip *
```
