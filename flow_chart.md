```mermaid
graph TD
    A[Start] --> B[User Input: Book Topic]
    
    %% Outline Generation
    B --> C[Generate Book Outline]
    C -->|Using GPT-4O| D[JSON Response]
    D -->|Parse| E[Structured Outline with Chapters & Research Questions]
    
    %% Parallel Research Process
    E --> F[Parallel Chapter Research]
    F --> G[Split into Batches]
    G --> H[Process Batch 1]
    G --> I[Process Batch 2]
    G --> J[Process Batch N]
    
    %% Research Details
    H & I & J -->|Using Perplexity API| K[Collect Research Data]
    
    %% Chapter Writing Process
    K --> L[Sequential Chapter Writing]
    L -->|Using GPT-4O-Mini| M[Write Chapter 1]
    M --> N[Update book.md]
    N --> O[Write Chapter 2]
    O --> P[Update book.md]
    P --> Q[Write Chapter N]
    Q --> R[Final Update book.md]
    
    %% Error Handling
    C & F & L -->|On Error| S[Error Handler]
    S -->|Log Error| T[Display Error Message]
    T --> U[Raise Exception]
    
    %% Completion
    R --> V[Book Creation Complete]
    
    %% Styling
    classDef api fill:#f9f,stroke:#333,stroke-width:2px
    classDef file fill:#bbf,stroke:#333,stroke-width:2px
    classDef process fill:#bfb,stroke:#333,stroke-width:2px
    classDef error fill:#fbb,stroke:#333,stroke-width:2px
    
    class C,H,I,J,M,O,Q api
    class D,N,P,R file
    class B,E,F,G,K,L process
    class S,T,U error
```

# Book Maker Process Flow

The above flow chart illustrates the complete process of the book maker application. Here's a breakdown of each major component:

1. **Initial Input**
   - User provides the book topic
   - System initializes with API keys and configurations

2. **Outline Generation**
   - GPT-4O generates a structured outline
   - Output includes chapters and research questions
   - Data is formatted in JSON for easy processing

3. **Parallel Research**
   - Chapters are processed in parallel batches
   - Each batch uses Perplexity API for research
   - Rate limiting and error handling are implemented

4. **Chapter Writing**
   - Sequential processing of chapters
   - GPT-4O-Mini writes each chapter
   - book.md is updated after each chapter completion

5. **Error Handling**
   - Comprehensive error catching at each stage
   - Colored console output for status updates
   - Graceful error recovery where possible

The process is designed to be efficient with parallel processing where possible, while maintaining data consistency and providing real-time updates to the user.