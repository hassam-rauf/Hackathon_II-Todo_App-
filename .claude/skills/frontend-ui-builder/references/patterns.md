# Frontend Patterns Reference

## Tailwind Utilities (Most Used)

### Layout
```
flex flex-col flex-row gap-2 gap-4 items-center justify-between
grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3
w-full max-w-md mx-auto p-4 md:p-6
```

### Typography
```
text-sm text-base text-lg text-xl text-2xl font-medium font-bold
text-gray-900 text-gray-600 text-gray-400
```

### Interactive
```
bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2
cursor-pointer transition-colors duration-200
disabled:opacity-50 disabled:cursor-not-allowed
```

### States
```
border border-gray-200 rounded-lg shadow-sm
focus:ring-2 focus:ring-blue-500 focus:outline-none
```

## Common Component Patterns

### Card
```tsx
<div className="bg-white border border-gray-200 rounded-lg shadow-sm p-4">
  <h3 className="font-medium text-gray-900">{title}</h3>
  <p className="text-sm text-gray-600 mt-1">{description}</p>
</div>
```

### Form Input
```tsx
<label className="block text-sm font-medium text-gray-700 mb-1">
  {label}
</label>
<input
  type="text"
  className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
  placeholder={placeholder}
  value={value}
  onChange={(e) => onChange(e.target.value)}
/>
```

### Button Variants
```tsx
// Primary
<button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">

// Secondary
<button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors">

// Danger
<button className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors">
```

### Empty State
```tsx
<div className="text-center py-12 text-gray-500">
  <p className="text-lg">No tasks yet</p>
  <p className="text-sm mt-1">Add a task to get started</p>
</div>
```

### Loading Skeleton
```tsx
<div className="animate-pulse space-y-4">
  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

### Toast/Notification
```tsx
<div className="fixed bottom-4 right-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg">
  Task created successfully
</div>
```
