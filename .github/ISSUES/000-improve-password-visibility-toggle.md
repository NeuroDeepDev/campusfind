Title: Improve Password Visibility Toggle Icon States

Description
-----------
The password visibility toggle icon is not visually intuitive. While an eye-slash icon is displayed, the distinction between the "show password" and "hide password" states is not sufficiently clear, which may cause confusion for users.

Current Behavior
----------------
- The password field displays an eye-slash icon.
- The icon styling and state transition are not obvious.
- Users may not immediately understand whether the password is currently visible or hidden.

Expected Behavior
-----------------
- When the password is hidden, display a clear **eye-slash (visibility_off)** icon.
- When the password is visible, display a standard **eye (visibility)** icon.
- The icon should switch dynamically when clicked.
- Add hover and focus states to indicate that the icon is interactive.

Suggested Improvement
---------------------
Use industry-standard visibility icons:

State | Icon | Meaning
---|---|---
Password Hidden | Eye with diagonal slash | Click to show password
Password Visible | Eye icon | Click to hide password

Benefits
--------
- Clear visual feedback for users
- Aligns with common UX patterns
- Improves accessibility and usability

Priority: Low-Medium
Type: Enhancement / UX Improvement
Labels: enhancement, ui, ux, login, accessibility, authentication

Notes
-----
Implementation should include keyboard focus styles and accessible `aria-label`/`title` updates when the state changes. Consider adding a small icon transition when toggling.
