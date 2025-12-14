### What is this

A fork of https://github.com/bumblebee4105/markers-puller, a python script to export The
Markers content as markdown, neatly organized in subdirectories. _The Markers_ was
a school software used by Open-ICT at Hogeschool Utrecht for several years. This
collaboration has ended after my first year in the study. The first-party PDF export was
deplorable, hence a student took the initiative to build a better one by scraping its API.
This was the original `markers-pullers`. I tried it, but noticed a few things I would've
done differently, hence I forked it and made some PRs to upstream.

Since HU students no longer have access to their _The Markers_ portoflios, this project
exists solely for posterity, and was an opportunity for me to practice managing
a simple Python project with Nix at the time.

The major difference with upstream, is that this fork will output all the files in
sub-directories by categories. So all peer feedback goes in `output/feedback`, all teacher
evaluations go to `output/evaluation`, check-ins to `output/checkin` etc.

I've also made small refactors to the code, and added a `flake.nix` with Nix managed
dependencies, and got rid of the dozens of screenshots in the README, as I expect a savvy
student to be familiar with the process.

### How to use

If you use Nix/NixOS for development, simply launch the development shell: `nix develop`
(or `direnv allow`, if you happen to use nix-direnv as well.)

Without Nix, install python & pip, create and start a virtual environment, and do
`pip install -r requirements.txt`

You should have a JSON file for each of your _The Markers_ collections. Since you can no
longer access _The Markers_, nothing can be done if you do not have them. They could be
retrieved by logging in to the website, looking at the web console, finding the API call
that would load the collection data (all of it, at once!!), and download & save it
a `markers.json`. Calling `python <path/to/this/repo/src/extract_markers.py>` in the same
folder as where `markers.json` is located, will then run the extraction process.
