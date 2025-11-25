# SonorAI

## Setup dev environment: 
1. Ensure Python 3.12-3.13 is installed (Python 3.13.9 is recommended)
2. Ensure \Users\<user>\AppData\Roaming\Python\Python313\Scripts is in PATH
3. Configure a local copy of the git repository
4. Setup the project Python environment:
   * py -3.13 -m pip install virtualenv
   * py -3.13 -m virtualenv sonoraienv
   * source sonoraienv/Scripts/activate
   * pip install -U -r requirements.txt
5. Setup the Django app and run a local server
   * py manage.py makemigrations SonorAI
   * py manage.py migrate
   * py manage.py runserver

## Using aiapp.py: 
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

example: &emsp; AudioAnalysis.audio_analysis(audio_file)
