
import torch
from typing import Any, Dict
from transformers import pipeline

class LLMConfig:
    def __init__(
        self,
        target_repr: str,
        sampling_strategy: str = "random",
        n_similar_examples: int = 5,
        cover_operators: bool = False,
        prompt_version: str = "v1",
        instruction_based: bool = False,
    ) -> None:
        self.target_repr = target_repr
        self.n_similar_examples = n_similar_examples
        self.cover_operators = cover_operators
        self.sampling_strategy = sampling_strategy
        self.prompt_version = prompt_version
        self.instruction_based = instruction_based

    @staticmethod
    def ablation_categories():
        return [
            "target_repr",
            "sampling_strategy",
            "n_similar_examples",
            "cover_operators",
            "prompt_version",
        ]

    @staticmethod
    def cat_to_human_readable(cat):
        return {
            "target_repr": "Target Representation",
            "sampling_strategy": "Sampling Strategy",
            "n_similar_examples": "Number of Similar Examples",
            "cover_operators": "Cover Operators",
            "prompt_version": "Prompt Version",
        }[cat]
    
    @staticmethod
    def repr_to_human_readable(repr):
        return {
            "asp_flat": "Flat ASP",
            "asp_nested": "Nested ASP",
            "asp_code": "Code-like ASP",
            "gqa": "GQA",
        }[repr]

    def get_ablation_values(self):
        return [self.__dict__[key] for key in self.ablation_categories()]

class HuggingFaceLLM():

    def __init__(
        self,
        config: LLMConfig,
        version: str = "HuggingFaceH4/zephyr-7b-alpha",
        name: str = None,
        inference_kwargs: Dict[str, Any] = {},
    ) -> None:
        super().__init__(config)
        self.pipe = pipeline(
            "text-generation",
            model=version,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.inference_kwargs = inference_kwargs
        self.inference_kwargs["pad_token_id"] = self.pipe.tokenizer.eos_token_id
        self.inference_kwargs["max_new_tokens"] = self._max_tokens
        self._name = name if name else version


    def generate(self, question: str) -> tuple[str, int]:
        output, nr_examples = self._generate(question)
        return self.post_process(output), nr_examples

    def _generate(self, question: str) -> tuple[str, int]:
        prompt, nr_examples = self.prompt_creator.get_prompt(question)
        messages = self.pipe.tokenizer.apply_chat_template(
            prompt, tokenize=False, add_generation_prompt=True
        )
        return self.pipe(messages, **self.inference_kwargs)[0]["generated_text"], nr_examples

    def post_process(self, output: str) -> str:
        output = output.split("<|assistant|>\n")[1]
        return self.cutoff_output(output)
