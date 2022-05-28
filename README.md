def ExitApp():
    MsgBox = messagebox.askquestion ('Exit App','Really Quit?',icon = 'error')
    if MsgBox == 'yes':
       self.window.destroy()
    else:
        messagebox.showinfo('Welcome Back','Welcome back to the App')
        
Button (root, text='Exit App',command=ExitApp).pack(side=BOTTOM)
