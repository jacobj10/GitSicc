# GitSicc
Tool for making drawings on your GitHub contributions graph!

## Install
Install from repository is as follow:
```bash
git clone https://github.com/jacobj10/GitSicc.git
cd GitSicc
pip install -r requirements.txt
```

## Running
`python3 sicc_window.py`

## Usage
First, enter the year you want the drawing to be drawn on in Git. It is recommended you use a blank year (i.e. one before you started using GitHub), as that will render the best results. While you can adjust the intensity in the application, **it does not render properly in the contribution graph**. Therefore, you are unfortunately restricted to mono color drawings. After selecting a valid year and creating your drawing, clicking export will create a repository called GitSicco in the cwd. After this, you have to add a remote to the repository with `git remote add origin https://github.com/YOUR_USERNAME/GitSicco.git`. Once this is done, create a repository called GitSicco **WITHOUT A README** on the GitHub web application, the push your changes up with `git push origin master`. Hopefully this works and you now have a sick drawing in your contribution graph.

See an example here: https://github.com/jacobj10?tab=overview&from=2010-12-01&to=2010-12-31
