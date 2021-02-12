class Info():

    def results(self):
        print("\n***RESULTS***")
        print("\nThe code produces 3 main results: a numerical score, another score out of 10, and a pass-fail mark. All of these results are subject to change based on various selected parameters.")
        print("\nThe numerical score exhibits the least variation. It will only change if the same sample is blurred using varying sigma values - this is the standard deviation, or severity, of Gaussian blurring. \nThis score is an exact value of the mean peak prominence across the entire sample. The mean peak prominence represents the difference between light intensity maxima, i.e. the contrast between the machine direction lines and 'background' of the sample.")
        print("\nThe score out of 10 is subject to whether or the sample is being compared to all samples of the same type, or only samples in a similar areal weight class. \nIt exists between 0 and 10, and indicates the severity of machine direction lines in the current sample, compared to samples with similar properties. \nHence, a score of 0 will indicate the poorest sample, whilst a score of 10 will indicate the best sample.")
        print("Note that the scaling for the score out of 10 was defined by the best and worst samples available at the time. This scaling can be subject to refinement with further data, and so currently testing samples beyond this defined range will produce a score outside the range of 0 to 10.")
        print("Testing against all samples of the same material (sample type) is recommended, since this gives a better appreciation for the visual severity of MD lines.")
        print("\nThe pass-fail mark indicates whether the sample 'passes' or 'fails' the test. This depends on whether the number score falls above or below a defined value which you will be later prompted to enter, with recommendations at the prompt.")
        print("\nA final note: there is an additional option to view plots of detected MD lines across one row of pixels. However this was implemented as part of the testing process, and is not fully developed. \nIf a visual representation of machine direction lines in a particular sample is required, looking directly at the sample is recommended!")
        print("\nFor further information, please contact the code authors through the project Github repository: https://github.com/msychung/Industrial-Group-Project \n")
    
    def workings(self):
        print("\n***WORKINGS***")
        print("\nThe linefinding process relies primarily on two Python modules: sci-kit image, and scipy signal. It is also dependent on several parameters, which you will be prompted to input throughout.")
        print("\nThe key constraint for the linefinding process is sample type, i.e. the material from which the sample is made. Sample scans of only one type can be entered per run of the code. This is due to the fact that a change in material produces very different results, and so samples of different material types cannot be directly compared.")
        print("\nSci-kit image is used to read the sample image in as a numpy array, which is a list of numbers. The sample then undergoes a Gaussian blur to smooth out and minimise noise.")
        print("\nVarious programs within the scipy signal module are used to find all of the peaks (representing MD lines) in all of the individual rows of the sample.")
        print("\nOnce all of the peaks in the sample have been found, the prominences (heights) of the peaks are calculated, to obtain the difference between the peak and 'background' of the sample.")
        print("\nThe bigger this difference, the more visible the corresponding machine direction lines are.")
        print("\nThe mean of all of the peak prominences is then calculated to determine the severity of machine direction lines in a sample, and assign a score to the sample.")
        print("\nFor further information, please contact the code authors, or view the code, through the project Github repository: https://github.com/msychung/Industrial-Group-Project \n")

    def information(self):
            question = input("Would you like to view information explaining this software? \nPlease respond 'yes' or no': ").lower()

            if not question in ('yes', 'no'):
                print("Sorry, that response was not recognised, please enter either 'yes' or 'no', and ensure correct spelling.\n")
                self.information()

            if question == 'yes':
                works_or_results = input('\nWould you like information regarding how the code works, what the results are, or both? \nPlease respond with "workings", "results", or "both". \nResponse: ').lower()

                if not works_or_results in ('workings', 'results', 'both'):
                    print('Response not recognised, please try again, and ensure correct spelling.')
                    self.information()

                elif works_or_results == 'results':
                    self.results()

                elif works_or_results == 'workings':
                    self.workings()

                else:    # works_or_results == 'both'
                    self.results()
                    self.workings()
                    
            else:
                print("\n")