import json
import numpy as np

from typing import Optional, List
from pathlib import Path
from dataclasses import dataclass # pip install dataclasses

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

# Internal classes
from . import encoders

# """Implementing the machine learning prediction model using classes"""
# class NotImplemented(Exception):

#     def implemented_error(self):
#         raise Exception("Not implemented")

@dataclass
class AIModel:
    model_path: Path
    tokenizer_path: Optional[Path] = None
    metadata_path: Optional[Path] = None

    model = None
    tokenizer = None
    metadata = None


    def __post__init__(self):
        if self.model_path.exists():
            self.model = load_model(self.model_path)
            print(self.model)
        if self.tokenizer_path.exists():
            if self.tokenizer_path.name.endswith("json"):
                tokenizer_text = self.tokenizer_path.read_text()
                self.tokenizer = tokenizer_from_json(tokenizer_text)
            else:
                raise Exception("Tokenizer file must be a json file")
        if self.metadata_path.exists():
            if self.metadata_path.name.endswith("json"):
                self.metadata = json.loads(self.metadata_path.read_text())
            else:
                raise Exception("metadata file must be a json file")

    def get_model(self):
        if not self.model:
            raise Exception("Model not implemented")
        return self.model
    
    def get_tokenizer(self):
        if not self.tokenizer:
            raise Exception("Tokenizer not implemented")
        return self.tokenizer
    
    def get_metadata(self):
        if not self.metadata:
            raise Exception("metadata not implemented")
        return self.metadata
    
    def get_sequences_from_text(self, texts: List[str]):
        tokenizer = self.get_tokenizer()
        sequences = tokenizer.texts_to_sequences(texts)
        return sequences

    def get_input_from_sequences(self, sequences):
        maxlen = self.get_metadata().get('max_sequence') or 280
        x_input = pad_sequences(sequences, maxlen=maxlen)
        return x_input
    
    def get_label_legend_inverted(self):
        legend = self.get_metadata().get('label_legend_inverted') or {}
        if len(legend.key()) != 2:
            raise Exception("Label legend must be a dictionary with 2 keys")
        return legend

    def get_label_pred(self, idx, val):
        legend = self.get_label_legend_inverted()
        return {
        "label": legend[str(idx)],
        "confidence": val}

    def get_top_pred_labeled(self, preds):
        top_index_value = np.argmax(preds) # get the top prediction value
        val = preds[top_index_value]
        top_pred = self.get_label_pred(top_index_value, val)
        return top_pred

    def predict_text(self, query:str, include_top=True, encode_to_json=True):
        model = self.get_model()
        sequences = self.get_sequences_from_text([query])
        x_input = self.get_input_from_sequences(sequences)
        preds = model.predict(x_input)
        labeled_preds = [self.get_label_pred(i, x) for i, x in enumerate(list(preds))]
        results = {
            "predictions": labeled_preds
        }
        if include_top:
            results['top'] = self.get_top_pred_labeled(preds)
        if encode_to_json:
            results = encoders.encode_to_json(results, as_py=True)
        return results