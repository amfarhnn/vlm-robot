# Prompt Engineering for Mobile Robot Navigation

`Prompt Engineering for Mobile Robot Navigation` is a research project focused on language-guided mobile robot navigation using large pre-trained models.

This project is centered on one primary paper:
- `LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action`

## Project Focus

The goal of this project is to study how a robot can follow natural language navigation instructions without relying on a language-annotated robot navigation dataset.

`LM-Nav` is a strong reference because it combines separate pre-trained models for:
- language understanding
- image-language grounding
- visual navigation
- long-horizon mobile robot navigation

## Selected Paper

| Paper | Authors | Venue | Publication | Code |
|---|---|---|---|---|
| LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action | Dhruv Shah, Blazej Osinski, Brian Ichter, Sergey Levine | CoRL / PMLR 2023 | [Paper](https://proceedings.mlr.press/v205/shah23b) | [Code](https://github.com/blazejosinski/lm_nav) |

## Project Documents

| Document | Description |
|---|---|
| [Chapter 2 Literature Review](literature_review.md) | Formal literature review chapter covering `LM-Nav` and related papers. |
| [Chapter 3 Methodology](chapter_3_methodology.md) | Formal methodology chapter following the university FYP chapter format. |

## Core Idea

`LM-Nav` builds a navigation system from three major components:

1. `GPT-3` extracts landmark names from a natural language instruction.
2. `CLIP` grounds those landmarks in visual observations from the environment.
3. `ViNG` navigates toward the grounded landmarks using a vision-based navigation policy.

This allows the robot to follow high-level language instructions while still using visual navigation models trained on large, unannotated trajectory datasets.

## Further Research

The papers below are useful for studying how `LM-Nav` can be extended or improved.

| Paper | Research Direction | How it relates to LM-Nav |
|---|---|---|
| [VLMaps: Visual Language Maps for Robot Navigation](https://vlmaps.github.io/) | Open-vocabulary spatial mapping | Improves language grounding by building maps that connect natural language queries to spatial locations. |
| [ViNT: A Foundation Model for Visual Navigation](https://proceedings.mlr.press/v229/shah23a.html) | Visual navigation foundation models | Provides a stronger modern navigation backbone that could replace older visual navigation modules such as ViNG. |
| [NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration](https://general-navigation-models.github.io/nomad/) | Diffusion-based navigation policies | Improves goal-directed navigation and exploration, especially in unseen environments. |
| [NaVid: Video-based VLM Plans the Next Step for Vision-and-Language Navigation](https://roboticsconference.org/2024/program/papers/79/) | VLM-based action planning | Uses video history and a VLM to plan next-step navigation actions from language instructions. |
| [Uni-NaVid: A Video-based Vision-Language-Action Model for Unifying Embodied Navigation Tasks](https://roboticsconference.org/program/papers/13/) | Vision-language-action navigation | Extends VLM navigation toward a unified model for instruction following, object search, tracking, and embodied question answering. |
| [NaVILA: Legged Robot Vision-Language-Action Model for Navigation](https://roboticsproceedings.org/rss21/p018.html) | Real-robot VLA navigation | Converts vision-language reasoning into movement commands for legged robot navigation. |
| [HOV-SG: Hierarchical Open-Vocabulary 3D Scene Graphs for Language-Grounded Robot Navigation](https://hovsg.github.io/) | 3D scene graph grounding | Improves long-horizon grounding by organizing rooms, objects, and floors into an open-vocabulary 3D scene graph. |
| [VLN-Zero](https://arxiv.org/abs/2509.18592) | Zero-shot navigation | Uses VLM-guided exploration and scene-graph memory to reduce repeated model calls and improve transfer. |
| [VLMnav: End-to-End Navigation with Vision Language Models](https://arxiv.org/abs/2411.05755) | Prompt-based action selection | Frames navigation as VLM question answering, which is closely related to prompt engineering for robot decisions. |
| [VLM-Nav: Mapless UAV Navigation Using Monocular Vision Driven by Vision-Language Models](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0345778) | Mapless VLM navigation | Explores recent VLM-based navigation for UAVs using monocular vision and zero-shot reasoning. |

## Research Roadmap

This project treats `LM-Nav` as the baseline system design. Its central pipeline is:

1. an LLM extracts landmarks from a natural language instruction
2. CLIP grounds those landmarks in visual observations
3. a navigation model executes movement toward the grounded goals

The further research papers are organized around possible improvements to this baseline:

- `VLMaps` and `HOV-SG` are used to study stronger spatial grounding. These methods improve how language is connected to maps, objects, rooms, and 3D scene structure.
- `ViNT` and `NoMaD` are used to study stronger navigation and action models. These methods provide more capable visual navigation backbones that could replace or extend the execution component in `LM-Nav`.
- `NaVid`, `Uni-NaVid`, and `NaVILA` are used to study the latest VLM and VLA navigation direction. These works move toward models that reason over vision, language, and action in a more integrated way.
- `VLMnav` is used as the main prompt-engineering reference because it studies how a vision-language model can choose navigation actions through a question-answering formulation.

## Methodology Notes

The main methodology for this project is based on [`LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action`](https://proceedings.mlr.press/v205/shah23b).

`LM-Nav` provides a clear modular approach for language-guided robot navigation:

1. use an LLM to extract landmark goals from natural language instructions
2. use CLIP to ground the extracted landmarks in visual observations
3. use a visual navigation model to execute movement toward the selected landmark

This methodology is suitable as the baseline because it connects prompt engineering, language understanding, image-text grounding, and mobile robot navigation in one complete pipeline.

Supporting methodology references:

| Paper | Methodology Role | Link |
|---|---|---|
| LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action | Main baseline methodology for landmark extraction, visual grounding, and navigation execution. | [Paper](https://proceedings.mlr.press/v205/shah23b) |
| VLMnav: End-to-End Navigation with Vision Language Models | Prompt-engineering methodology for choosing robot navigation actions through a VLM question-answering formulation. | [Paper](https://arxiv.org/abs/2411.05755) |
| VLMaps: Visual Language Maps for Robot Navigation | Spatial grounding methodology using open-vocabulary visual-language maps. | [Project](https://vlmaps.github.io/) |
| HOV-SG: Hierarchical Open-Vocabulary 3D Scene Graphs for Language-Grounded Robot Navigation | Spatial reasoning methodology using hierarchical 3D scene graphs. | [Project](https://hovsg.github.io/) |
| ViNT: A Foundation Model for Visual Navigation | Navigation model methodology for stronger visual navigation execution. | [Paper](https://proceedings.mlr.press/v229/shah23a.html) |
| NoMaD: Goal Masked Diffusion Policies for Navigation and Exploration | Navigation policy methodology using diffusion-based goal-directed navigation. | [Project](https://general-navigation-models.github.io/nomad/) |

## Research Direction

This project will use `LM-Nav` as the main reference for understanding:
- how natural language instructions can be converted into landmark-based navigation goals
- how vision-language models can connect text landmarks to visual observations
- how pre-trained models can be combined without fine-tuning
- how long-horizon robot navigation can be performed from language commands
- how newer VLM, VLA, mapping, and navigation-policy methods can improve the original `LM-Nav` pipeline

## Project Goals

Possible goals for this repository include:
- summarizing the `LM-Nav` method and architecture
- reproducing a simplified version of the language-to-landmark pipeline
- experimenting with image-text grounding using CLIP or a modern VLM
- documenting the navigation pipeline, assumptions, and limitations
- comparing landmark-based navigation with simpler goal-selection baselines
- reviewing later research papers that improve landmark grounding, spatial reasoning, or navigation execution

## Notes

- This README is intentionally focused on the selected `LM-Nav` paper.
- Additional papers can be added later only if they directly support this research direction.
- The original paper appears in `Proceedings of Machine Learning Research`, volume 205, pages 492-504.
