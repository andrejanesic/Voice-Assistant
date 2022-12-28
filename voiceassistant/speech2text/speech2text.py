from voiceassistant.core.iaudio import IAudio
import torch
import torchaudio

torch.random.manual_seed(0)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

SPEECH_FILE = 'Voice-Assistant/audiorecords/audio1.wav'

bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H 
model = bundle.get_model().to(device) 

class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission: torch.Tensor) -> str:
        """Given a sequence emission over labels, get the best path string
        Args:
          emission (Tensor): Logit tensors. Shape `[num_seq, num_label]`.

        Returns:
          str: The resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])

# def retrainModel():
    #retrain and save model
    

def generateText(speech: IAudio) -> str:
          
    print(model.__class__) #<class 'torchaudio.models.wav2vec2.model.Wav2Vec2Model'>

    # waveform, sample_rate = torchaudio.load(SPEECH_FILE)
    # waveform = waveform.to(device)

    # if sample_rate != bundle.sample_rate:
    #     waveform = torchaudio.functional.resample(waveform, sample_rate, bundle.sample_rate)    

    sample_frame_rate = speech.get_framerate()
    waveform, sample_rate = torchaudio.load(SPEECH_FILE)
    waveform = waveform.to(device)

    if sample_frame_rate != bundle.sample_rate:
        waveform = torchaudio.functional.resample(waveform, sample_frame_rate, bundle.sample_rate)  

    with torch.inference_mode():
        emission, _ = model(waveform)

    #decoder = GreedyCTCDecoder(labels=bundle.get_labels())
    decoder = GreedyCTCDecoder(labels=speech.get_values())
    transcript = decoder(emission[0])
    return transcript

    
