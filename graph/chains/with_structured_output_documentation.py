#  @overload  # type: ignore[override]
#     def with_structured_output(
#         self,
#         schema: Optional[_DictOrPydanticClass] = None,
#         *,
#         method: Literal["function_calling", "json_mode"] = "function_calling",
#         include_raw: Literal[True] = True,
#         **kwargs: Any,
#     ) -> Runnable[LanguageModelInput, _AllReturnType]: ...

#     @overload
#     def with_structured_output(
#         self,
#         schema: Optional[_DictOrPydanticClass] = None,
#         *,
#         method: Literal["function_calling", "json_mode"] = "function_calling",
#         include_raw: Literal[False] = False,
#         **kwargs: Any,
#     ) -> Runnable[LanguageModelInput, _DictOrPydantic]: ...

#     def with_structured_output(
#         self,
#         schema: Optional[_DictOrPydanticClass] = None,
#         *,
#         method: Literal["function_calling", "json_mode"] = "function_calling",
#         include_raw: bool = False,
#         **kwargs: Any,
#     ) -> Runnable[LanguageModelInput, _DictOrPydantic]:
#         """Model wrapper that returns outputs formatted to match the given schema.

#         Args:
#             schema:
#                 The output schema. Can be passed in as:
#                     - an OpenAI function/tool schema,
#                     - a JSON Schema,
#                     - a TypedDict class (support added in 0.1.20),
#                     - or a Pydantic class.
#                 If ``schema`` is a Pydantic class then the model output will be a
#                 Pydantic instance of that class, and the model-generated fields will be
#                 validated by the Pydantic class. Otherwise the model output will be a
#                 dict and will not be validated. See :meth:`langchain_core.utils.function_calling.convert_to_openai_tool`
#                 for more on how to properly specify types and descriptions of
#                 schema fields when specifying a Pydantic or TypedDict class.

#                 .. versionchanged:: 0.1.20

#                         Added support for TypedDict class.

#             method:
#                 The method for steering model generation, either "function_calling"
#                 or "json_mode". If "function_calling" then the schema will be converted
#                 to an OpenAI function and the returned model will make use of the
#                 function-calling API. If "json_mode" then OpenAI's JSON mode will be
#                 used. Note that if using "json_mode" then you must include instructions
#                 for formatting the output into the desired schema into the model call.
#             include_raw:
#                 If False then only the parsed structured output is returned. If
#                 an error occurs during model output parsing it will be raised. If True
#                 then both the raw model response (a BaseMessage) and the parsed model
#                 response will be returned. If an error occurs during output parsing it
#                 will be caught and returned as well. The final output is always a dict
#                 with keys "raw", "parsed", and "parsing_error".

#         Returns:
#             A Runnable that takes same inputs as a :class:`langchain_core.language_models.chat.BaseChatModel`.

#             If ``include_raw`` is False and ``schema`` is a Pydantic class, Runnable outputs
#             an instance of ``schema`` (i.e., a Pydantic object).

#             Otherwise, if ``include_raw`` is False then Runnable outputs a dict.

#             If ``include_raw`` is True, then Runnable outputs a dict with keys:
#                 - ``"raw"``: BaseMessage
#                 - ``"parsed"``: None if there was a parsing error, otherwise the type depends on the ``schema`` as described above.
#                 - ``"parsing_error"``: Optional[BaseException]

#         Example: schema=Pydantic class, method="function_calling", include_raw=False:
#             .. code-block:: python

#                 from typing import Optional

#                 from langchain_openai import ChatOpenAI
#                 from langchain_core.pydantic_v1 import BaseModel, Field


#                 class AnswerWithJustification(BaseModel):
#                     '''An answer to the user question along with justification for the answer.'''

#                     answer: str
#                     # If we provide default values and/or descriptions for fields, these will be passed
#                     # to the model. This is an important part of improving a model's ability to
#                     # correctly return structured outputs.
#                     justification: Optional[str] = Field(
#                         default=None, description="A justification for the answer."
#                     )


#                 llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
#                 structured_llm = llm.with_structured_output(AnswerWithJustification)

#                 structured_llm.invoke(
#                     "What weighs more a pound of bricks or a pound of feathers"
#                 )

#                 # -> AnswerWithJustification(
#                 #     answer='They weigh the same',
#                 #     justification='Both a pound of bricks and a pound of feathers weigh one pound. The weight is the same, but the volume or density of the objects may differ.'
#                 # )

#         Example: schema=Pydantic class, method="function_calling", include_raw=True:
#             .. code-block:: python

#                 from langchain_openai import ChatOpenAI
#                 from langchain_core.pydantic_v1 import BaseModel


#                 class AnswerWithJustification(BaseModel):
#                     '''An answer to the user question along with justification for the answer.'''

#                     answer: str
#                     justification: str


#                 llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
#                 structured_llm = llm.with_structured_output(
#                     AnswerWithJustification, include_raw=True
#                 )

#                 structured_llm.invoke(
#                     "What weighs more a pound of bricks or a pound of feathers"
#                 )
#                 # -> {
#                 #     'raw': AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_Ao02pnFYXD6GN1yzc0uXPsvF', 'function': {'arguments': '{"answer":"They weigh the same.","justification":"Both a pound of bricks and a pound of feathers weigh one pound. The weight is the same, but the volume or density of the objects may differ."}', 'name': 'AnswerWithJustification'}, 'type': 'function'}]}),
#                 #     'parsed': AnswerWithJustification(answer='They weigh the same.', justification='Both a pound of bricks and a pound of feathers weigh one pound. The weight is the same, but the volume or density of the objects may differ.'),
#                 #     'parsing_error': None
#                 # }

#         Example: schema=TypedDict class, method="function_calling", include_raw=False:
#             .. code-block:: python

#                 # IMPORTANT: If you are using Python <=3.8, you need to import Annotated
#                 # from typing_extensions, not from typing.
#                 from typing_extensions import Annotated, TypedDict

#                 from langchain_openai import ChatOpenAI


#                 class AnswerWithJustification(TypedDict):
#                     '''An answer to the user question along with justification for the answer.'''

#                     answer: str
#                     justification: Annotated[
#                         Optional[str], None, "A justification for the answer."
#                     ]


#                 llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
#                 structured_llm = llm.with_structured_output(AnswerWithJustification)

#                 structured_llm.invoke(
#                     "What weighs more a pound of bricks or a pound of feathers"
#                 )
#                 # -> {
#                 #     'answer': 'They weigh the same',
#                 #     'justification': 'Both a pound of bricks and a pound of feathers weigh one pound. The weight is the same, but the volume and density of the two substances differ.'
#                 # }

#         Example: schema=OpenAI function schema, method="function_calling", include_raw=False:
#             .. code-block:: python

#                 from langchain_openai import ChatOpenAI

#                 oai_schema = {
#                     'name': 'AnswerWithJustification',
#                     'description': 'An answer to the user question along with justification for the answer.',
#                     'parameters': {
#                         'type': 'object',
#                         'properties': {
#                             'answer': {'type': 'string'},
#                             'justification': {'description': 'A justification for the answer.', 'type': 'string'}
#                         },
#                        'required': ['answer']
#                    }
#                }

#                 llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
#                 structured_llm = llm.with_structured_output(oai_schema)

#                 structured_llm.invoke(
#                     "What weighs more a pound of bricks or a pound of feathers"
#                 )
#                 # -> {
#                 #     'answer': 'They weigh the same',
#                 #     'justification': 'Both a pound of bricks and a pound of feathers weigh one pound. The weight is the same, but the volume and density of the two substances differ.'
#                 # }

#         Example: schema=Pydantic class, method="json_mode", include_raw=True:
#             .. code-block::

#                 from langchain_openai import ChatOpenAI
#                 from langchain_core.pydantic_v1 import BaseModel

#                 class AnswerWithJustification(BaseModel):
#                     answer: str
#                     justification: str

#                 llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
#                 structured_llm = llm.with_structured_output(
#                     AnswerWithJustification,
#                     method="json_mode",
#                     include_raw=True
#                 )

#                 structured_llm.invoke(
#                     "Answer the following question. "
#                     "Make sure to return a JSON blob with keys 'answer' and 'justification'.\n\n"
#                     "What's heavier a pound of bricks or a pound of feathers?"
#                 )
#                 # -> {
#                 #     'raw': AIMessage(content='{\n    "answer": "They are both the same weight.",\n    "justification": "Both a pound of bricks and a pound of feathers weigh one pound. The difference lies in the volume and density of the materials, not the weight." \n}'),
#                 #     'parsed': AnswerWithJustification(answer='They are both the same weight.', justification='Both a pound of bricks and a pound of feathers weigh one pound. The difference lies in the volume and density of the materials, not the weight.'),
#                 #     'parsing_error': None
#                 # }

#         Example: schema=None, method="json_mode", include_raw=True:
#             .. code-block::

#                 structured_llm = llm.with_structured_output(method="json_mode", include_raw=True)

#                 structured_llm.invoke(
#                     "Answer the following question. "
#                     "Make sure to return a JSON blob with keys 'answer' and 'justification'.\n\n"
#                     "What's heavier a pound of bricks or a pound of feathers?"
#                 )
#                 # -> {
#                 #     'raw': AIMessage(content='{\n    "answer": "They are both the same weight.",\n    "justification": "Both a pound of bricks and a pound of feathers weigh one pound. The difference lies in the volume and density of the materials, not the weight." \n}'),
#                 #     'parsed': {
#                 #         'answer': 'They are both the same weight.',
#                 #         'justification': 'Both a pound of bricks and a pound of feathers weigh one pound. The difference lies in the volume and density of the materials, not the weight.'
#                 #     },
#                 #     'parsing_error': None
#                 # }
#         """  # noqa: E501
#         if kwargs:
#             raise ValueError(f"Received unsupported arguments {kwargs}")
#         is_pydantic_schema = _is_pydantic_class(schema)
#         if method == "function_calling":
#             if schema is None:
#                 raise ValueError(
#                     "schema must be specified when method is 'function_calling'. "
#                     "Received None."
#                 )
#             tool_name = convert_to_openai_tool(schema)["function"]["name"]
#             llm = self.bind_tools(
#                 [schema], tool_choice=tool_name, parallel_tool_calls=False
#             )
#             if is_pydantic_schema:
#                 output_parser: OutputParserLike = PydanticToolsParser(
#                     tools=[schema],  # type: ignore[list-item]
#                     first_tool_only=True,  # type: ignore[list-item]
#                 )
#             else:
#                 output_parser = JsonOutputKeyToolsParser(
#                     key_name=tool_name, first_tool_only=True
#                 )
#         elif method == "json_mode":
#             llm = self.bind(response_format={"type": "json_object"})
#             output_parser = (
#                 PydanticOutputParser(pydantic_object=schema)  # type: ignore[arg-type]
#                 if is_pydantic_schema
#                 else JsonOutputParser()
#             )
#         else:
#             raise ValueError(
#                 f"Unrecognized method argument. Expected one of 'function_calling' or "
#                 f"'json_mode'. Received: '{method}'"
#             )

#         if include_raw:
#             parser_assign = RunnablePassthrough.assign(
#                 parsed=itemgetter("raw") | output_parser, parsing_error=lambda _: None
#             )
#             parser_none = RunnablePassthrough.assign(parsed=lambda _: None)
#             parser_with_fallback = parser_assign.with_fallbacks(
#                 [parser_none], exception_key="parsing_error"
#             )
#             return RunnableMap(raw=llm) | parser_with_fallback
#         else:
#             return llm | output_parser

