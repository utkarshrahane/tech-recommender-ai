from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
import operator

# --- INPUT MODEL ---
class ProductRequest(BaseModel):
    category: str = Field(description="The type of product, e.g., Smartphone")
    budget: int = Field(description="Maximum budget in INR")
    priority: str = Field(description="The user's main focus, e.g., Camera")

# --- DATA MODELS ---
class ScoutedProduct(BaseModel):
    name: str
    price: str
    specs: dict
    pros: List[str]
    source_url: str

class TechnicalSpecs(BaseModel):
    product_name: str
    antutu_score: Optional[int]
    chipset: str
    camera_sensor: str
    ois_support: bool

# --- AGENT OUTPUT SCHEMAS (Missing Classes) ---
class ResearchOutput(BaseModel):
    """The structured output from the Researcher Agent"""
    products: List[ScoutedProduct] = Field(description="List of products found with their raw details.")

class AnalystOutput(BaseModel):
    """The structured output from the Analyst Agent"""
    top_picks: List[ScoutedProduct]
    rationale: str

class BenchmarkOutput(BaseModel):
    """The structured output from the Benchmarker Agent"""
    specs: List[TechnicalSpecs] = Field(description="Technical benchmarks for the shortlisted products.")

# --- SHARED GRAPH STATE ---
from typing import TypedDict

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    request: ProductRequest             # Validated Input
    shortlist: List[ScoutedProduct]     # List of Pydantic objects
    benchmarks: List[TechnicalSpecs]    # List of Technical objects
    final_report: str
    