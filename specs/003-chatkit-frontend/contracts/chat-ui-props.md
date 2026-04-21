# UI Contract: Chat Component Props

**Feature**: 003-chatkit-frontend | **Date**: 2026-04-08

## ChatPanel

```typescript
interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
  onTasksChanged: () => void;  // Called when AI performs tool calls
}
```

## ChatMessages

```typescript
interface ChatMessagesProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

interface ChatMessage {
  id: number | string;       // number from DB, string for optimistic
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCall[];    // Only on assistant messages
  createdAt: string;
}

interface ToolCall {
  tool: string;
  args: Record<string, unknown>;
  result: Record<string, unknown>;
}
```

## ChatInput

```typescript
interface ChatInputProps {
  onSend: (message: string) => void;
  disabled: boolean;
  isLoading: boolean;
}
```

## ChatConversationSelector

```typescript
interface ChatConversationSelectorProps {
  conversations: ChatConversation[];
  activeId: number | null;
  onSelect: (id: number | null) => void;  // null = new conversation
  loading: boolean;
}

interface ChatConversation {
  id: number;
  preview: string;
  updatedAt: string;
}
```

## ToolCallChip

```typescript
interface ToolCallChipProps {
  toolCall: ToolCall;
}
```

## API Client Extensions (lib/api.ts)

```typescript
// New methods added to the api object
interface ApiExtensions {
  getConversations: (userId: string) => Promise<ChatConversation[]>;
  getMessages: (userId: string, conversationId: number) => Promise<ChatMessage[]>;
  sendChatMessage: (
    userId: string,
    message: string,
    conversationId?: number
  ) => Promise<{
    conversation_id: number;
    response: string;
    tool_calls: ToolCall[];
  }>;
}
```
