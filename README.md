
# HashVault

## Generating a New SSH Key for GitHub

Follow these steps to generate a new SSH key and add it to your GitHub account.

### 1. Generate a New SSH Key

1. Open your terminal and run the following command to generate a new SSH key:

   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

   - Replace `your_email@example.com` with your GitHub email.
   - When prompted for a file to save the key, press **Enter** to accept the default location, or specify a different file path if desired. The default location is `~/.ssh/id_rsa`.

2. If prompted to enter a passphrase, you can either set a passphrase for added security or leave it blank by pressing **Enter**.

### 2. Add the SSH Key to the SSH Agent

To ensure your SSH key is added to the SSH agent, follow these steps:

1. Start the SSH agent:

   ```bash
   eval "$(ssh-agent -s)"
   ```

2. Add the SSH private key to the SSH agent:

   ```bash
   ssh-add ~/.ssh/id_rsa
   ```

   If you saved the SSH key under a different name or location, replace `id_rsa` with the appropriate filename.

### 3. Add Your SSH Key to GitHub

1. Display the SSH public key by running:

   ```bash
   cat ~/.ssh/id_rsa.pub
   ```

2. Copy the entire output of the above command.

3. Go to **GitHub**:
   - In the upper-right corner of any page, click your profile photo, then click **Settings**.
   - In the left sidebar, click **SSH and GPG keys**.
   - Click the **New SSH key** button.
   - Paste your SSH public key into the "Key" field and give it a title (e.g., "My SSH Key").
   - Click **Add SSH key**.

### 4. Test the SSH Connection

To ensure everything is working correctly, run the following command:

```bash
ssh -T git@github.com
```

You should see a message like this:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

### 5. Update Your Git Remote URL (if needed)

If your repository is already set up with a different SSH key or URL, you may need to update the remote URL to use the new SSH key.

1. To check your current remote URL, run:

   ```bash
   git remote -v
   ```

2. If needed, update the remote URL to the new SSH URL:

   ```bash
   git remote set-url origin git@github.com:YourUsername/YourRepository.git
   ```

Replace `YourUsername` and `YourRepository` with the correct GitHub username and repository name.

---

Now you should be able to use the new SSH key for GitHub operations such as cloning, pushing, and pulling.
