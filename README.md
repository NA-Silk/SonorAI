# SonorAI

1. Initial setup: <br>
pip install --upgrade distro-info <br>
pip3 install --upgrade pip <br>
pip install -U -r requirements.txt <br>

* Troubleshooting: <br>
pip install django <br>
pip install wheel <br>
pip install psycopg2 <br>
pip install psycopg2-binary <br>
pip install django.db <br>

2. Dev commands: <br>
python manage.py makemigrations <br>
python manage.py migrate <br>

* Using aiapp.py:                              <br>

(class) AudioAnalysis                          <br>
(method) def audio_analysis(                   <br>
    &emsp; audio_file,                         <br>
    &emsp; output_path: str = "out.musicxml",  <br>
    &emsp; title: str = "Untitled document",   <br>
    &emsp; epsilon: float = 1e-8,              <br>
    &emsp; confidence_threshold: float = 0.55, <br>
    &emsp; min_length: float = 0.03,           <br>
    &emsp; delta: float = 0.005                <br>
) -> output_path: MusicXML                     <br>

ex) <br>
    &emsp; AudioAnalysis.audio_analysis(audio_file)
