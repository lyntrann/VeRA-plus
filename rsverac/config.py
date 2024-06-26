# coding=utf-8
# Copyright 2023-present the HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass, field
from typing import List, Optional, Union

from peft.config import PeftConfig
from peft.utils import PeftType
PeftType.VERA = "VERA"

@dataclass
class VeraConfig(PeftConfig):
    """
    This is the configuration class to store the configuration of a [`VeraModel`].

    Args:
        r (`int`): Vera attention dimension.
        target_modules (`Union[List[str],str]`): The names of the modules to apply Vera to.
        projection_prng_key:
            (`Optional[int]`): Vera PRNG init key. Used for initialising vera_A and vera_B for new models, or when the
            checkpoint
        did not include these projections.
        save_projection (`bool`):
            Whether to save the vera_A / vera_B projections in the state dict alongside per layer lambda_b / lambda_d
            weights. This will increase the size of the checkpoint, but guarantee that we can reload the checkpoint on
            all system configurations. Defaults to `True`.
        vera_dropout (`float`): The dropout probability for Vera layers.
        d_initial (`float`): Initial init value for `vera_lambda_d` vector used when `init_vera_weights`.
        fan_in_fan_out (`bool`): Set this to True if the layer to replace stores weight like (fan_in, fan_out).
            For example, gpt-2 uses `Conv1D` which stores weights like (fan_in, fan_out) and hence this should be set
            to `True`.
        bias (`str`): Bias type for Vera. Can be 'none', 'all' or 'vera_only'. If 'all' or 'vera_only', the
            corresponding biases will be updated during training. Be aware that this means that, even when disabling
            the adapters, the model will not produce the same output as the base model would have without adaptation.
        modules_to_save (`List[str]`):List of modules apart from Vera layers to be set as trainable
            and saved in the final checkpoint.
        layers_to_transform (`Union[List[int],int]`):
            The layer indexes to transform, if this argument is specified, it will apply the Vera transformations on
            the layer indexes that are specified in this list. If a single integer is passed, it will apply the Vera
            transformations on the layer at this index.
        layers_pattern (`str`):
            The layer pattern name, used only if `layers_to_transform` is different from `None` and if the layer
            pattern is not in the common layers pattern.
    """

    r: int = field(default=8, metadata={"help": "Vera attention dimension"})
    target_modules: Optional[Union[List[str], str]] = field(
        default=None,
        metadata={
            "help": (
                "List of module names or regex expression of the module names to replace with Vera."
                "For example, ['q', 'v'] or '.*decoder.*(SelfAttention|EncDecAttention).*(q|v)$' "
            )
        },
    )
    vera_alpha: int = field(default=8, metadata={"help": "Vera alpha"})
    use_rsvera: bool = field(
        default=False,
        metadata={
            "help": (
                "When set to True, uses Rank-Stabilized LoRA doi.org/10.48550/arXiv.2312.03732"
                " which sets the adapter scaling factor to `vera_alpha/math.sqrt(r)`, since it"
                " was proven to work better. Otherwise, it will use the original default"
                " value of `vera_alpha/r`."
            )
        },
    )
    projection_prng_key: Optional[int] = field(
        default=None,
        metadata={
            "help": (
                "Vera PRNG init key. Used for initialising vera_A and vera_B for new models, or when the checkpoint"
                " did not include these projections. This value cannot be set to `None`."
            )
        },
    )
    save_projection: bool = field(
        default=True,
        metadata={
            "help": (
                "Whether to save the vera_A / vera_B projections in the state dict alongside per layer lambda_b /"
                " lambda_d weights. This will increase the size of the checkpoint, but guarantee that we can reload"
                " the checkpoint on all system configurations."
            )
        },
    )
    vera_dropout: float = field(default=0.0, metadata={"help": "Vera dropout"})
    d_initial: float = field(default=1.0, metadata={"help": "Initial init value for d vector."})
    c_initial: float = field(default=1.0, metadata={"help": "Initial init value for c vector."})
    fan_in_fan_out: bool = field(
        default=False,
        metadata={"help": "Set this to True if the layer to replace stores weight like (fan_in, fan_out)"},
    )
    bias: str = field(default="none", metadata={"help": "Bias type for Vera. Can be 'none', 'all' or 'vera_only'"})
    modules_to_save: Optional[List[str]] = field(
        default=None,
        metadata={
            "help": (
                "List of modules apart from Vera layers to be set as trainable and saved in the final checkpoint. For"
                " example, in Sequence Classification or Token Classification tasks, the final layer"
                " `classifier/score` are randomly initialized and as such need to be trainable and saved."
            )
        },
    )
    init_vera_weights: bool = field(
        default=True,
        metadata={
            "help": (
                "Whether to initialize the weights of the Vera layers with their default initialization. Don't change "
                "this setting, except if you know exactly what you're doing."
            ),
        },
    )
    layers_to_transform: Optional[Union[List[int], int]] = field(
        default=None,
        metadata={
            "help": (
                "The layer indexes to transform, is this argument is specified, PEFT will transform only the layers"
                " indexes that are specified inside this list. If a single integer is passed, PEFT will transform only"
                " the layer at this index."
            )
        },
    )
    layers_pattern: Optional[str] = field(
        default=None,
        metadata={
            "help": (
                "The layer pattern name, used only if `layers_to_transform` is different to None and if the layer"
                " pattern is not in the common layers pattern."
            )
        },
    )
    rank_pattern: Optional[dict] = field(
        default_factory=dict,
        metadata={
            "help": (
                "The mapping from layer names or regexp expression to ranks which are different from the default rank specified by `r`. "
                "For example, `{model.decoder.layers.0.encoder_attn.k_proj: 8`}"
            )
        },
    )
    alpha_pattern: Optional[dict] = field(
        default_factory=dict,
        metadata={
            "help": (
                "The mapping from layer names or regexp expression to alphas which are different from the default alpha specified by `lora_alpha`. "
                "For example, `{model.decoder.layers.0.encoder_attn.k_proj: 32`}"
            )
        },
    )

    def __post_init__(self):
        self.peft_type = PeftType.VERA
        self.target_modules = (
            set(self.target_modules) if isinstance(self.target_modules, list) else self.target_modules
        )