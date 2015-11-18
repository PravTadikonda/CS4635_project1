# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import itertools;
NUM_OF_ANSWERS = 6;

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        if (problem.problemType != '2x2'):
            print "ERROR: We do not support", problem.problemType, "matracies!";
        
        figures = problem.figures;
        aObjects = figures['A'].objects;
        bObjects = figures['B'].objects;
        cObjects = figures['C'].objects;

        relationFrame = {};
        relationFrame['A-B'] = {};
        relationFrame['A-C'] = {};
        numOfObjsAB = self.changeInObjects(aObjects, bObjects);

        bestLink = self.getBestLinks(aObjects, bObjects);
        links = bestLink[0].split(', ');
        # print links
        for link in links:
            if link[0] in aObjects:
                firstObjectAttr = figures['A'].objects[link[0]].attributes;
                secondObjectAttr = figures['B'].objects[link[2]].attributes;
            else:
                firstObjectAttr = figures['A'].objects[link[2]].attributes;
                secondObjectAttr = figures['B'].objects[link[0]].attributes;

            relationFrame['A-B'][link] = self.getDictOfRelation(firstObjectAttr, secondObjectAttr);

        bestLink = self.getBestLinks(aObjects, cObjects);
        links = bestLink[0].split(', ');
        for link in links:
            if link[0] in aObjects:
                firstObjectAttr = figures['A'].objects[link[0]].attributes;
                secondObjectAttr = figures['C'].objects[link[2]].attributes;
            else:
                firstObjectAttr = figures['A'].objects[link[2]].attributes;
                secondObjectAttr = figures['C'].objects[link[0]].attributes;

            relationFrame['A-C'][link] = self.getDictOfRelation(firstObjectAttr, secondObjectAttr);

        tempRelation = {};
        tempRelation['C-D'] = {};
        # tempRelation['B-D'] = {};

        numOfObjsCD = {};
        for num in range(1, (NUM_OF_ANSWERS + 1)):
            currAnsObjects = figures[str(num)].objects;
            numOfObjsCD[num] = self.changeInObjects(cObjects, currAnsObjects);
            bestLink = self.getBestLinks(cObjects, currAnsObjects);
            links = bestLink[0].split(', ');

            currAnsGroup = {};
            for link in links:
                if link[0] in cObjects:
                    firstObjectAttr = figures['C'].objects[link[0]].attributes;
                    secondObjectAttr = figures[str(num)].objects[link[2]].attributes;
                else:
                    firstObjectAttr = figures['C'].objects[link[2]].attributes;
                    secondObjectAttr = figures[str(num)].objects[link[0]].attributes;
                currAnsGroup[link] = self.getDictOfRelation(firstObjectAttr, secondObjectAttr);
            tempRelation['C-D'][num] = currAnsGroup;

        abRelation = relationFrame['A-B'];
        acRelation = relationFrame['A-C'];
        cdRelation = tempRelation['C-D'];

        similarities = {};
        for answers in cdRelation:
            totalVal = 0;
            for val in acRelation.keys():
                x = val[0];
                y = val[2];
                for fir in abRelation.keys():
                    if x in fir:
                        if fir[0] == x:
                            for sec in cdRelation[answers].keys():
                                if y in sec:
                                    totalVal = totalVal + self.calculateSimilarValue(abRelation[fir], cdRelation[answers][sec]);
                        elif fir[2] == x:
                            for sec in cdRelation[answers].keys():
                                if y in sec:
                                    totalVal = totalVal + self.calculateSimilarValue(abRelation[fir], cdRelation[answers][sec]);
                    elif y in fir:
                        if fir[0] == y:
                            for sec in cdRelation[answers].keys():
                                if x in sec:
                                    totalVal = totalVal + self.calculateSimilarValue(abRelation[fir], cdRelation[answers][sec]);
                        elif fir[2] == y:
                            for sec in cdRelation[answers].keys():
                                if x in sec:
                                    totalVal = totalVal + self.calculateSimilarValue(abRelation[fir], cdRelation[answers][sec]);
            
            if (len(numOfObjsCD[answers]) is not 0) and (len(numOfObjsAB) is not 0):
                # print numOfObjsCD[answers]
                if (numOfObjsCD[answers][0] == numOfObjsAB[0]) and (numOfObjsCD[answers][1] == numOfObjsAB[1]):
                    totalVal = totalVal + numOfObjsAB[1];
            similarities[answers] = totalVal;
        
        #TODO: deal with ties, instead of picking the first one
        answer = max(similarities, key=lambda i: similarities[i]);

        if problem.checkAnswer(answer) is answer:
            print problem.name, '- right answer'
            return answer;
        else:
            print 'wrong answer'
            return -1;

    #TODO: create a cleaner way to see the change of number of objects (too many parameters)
    def getBestLinks(self, listOfObjsA, listOfObjsB):
        chosen = self.chooseLargerDict(listOfObjsA, listOfObjsB);
        largerList = chosen['larger'];
        smallerList = chosen ['smaller'];

        numOfComb = list(itertools.combinations(largerList.keys(), len(smallerList)));
        numOfPerm = list(itertools.permutations(smallerList.keys()));

        listOfPairs = [];
        for c in numOfComb:
            for p in numOfPerm:
                getGroups = self.createLinkGroups(c, largerList, p, smallerList, listOfObjsA, listOfObjsB);
                listOfPairs = listOfPairs + [getGroups];
        return sorted(listOfPairs, key=lambda listOfPairs:listOfPairs[1], reverse=True)[0];

    #TODO: make this a learning priority list
    def createLinkGroups(self, combTup, comObj, permTup, permObj, listA, listB):
        if len(combTup) is not len(permTup):
            print 'OOOPPSSSS!!!!!!'

        thisPair = "";
        totalVal = 0;

        for ind in range(len(combTup)):
            c = combTup[ind];
            p = permTup[ind];
            thisPair = thisPair + c + '-' + p;
            if ind < (len(combTup) - 1):
                thisPair = thisPair + ', ';

            comAttr = comObj[c].attributes;
            permAttr = permObj[p].attributes;

            #TODO: make this a for-loop
            if ('size' in comAttr) and ('size' in permAttr):
                if comAttr['size'] == permAttr['size']:
                    totalVal = totalVal + 4;
            if ('shape' in comAttr) and ('shape' in permAttr):
                if comAttr['shape'] == permAttr['shape']:
                    totalVal = totalVal + 3;
            if ('angle' in comAttr) and ('angle' in permAttr):
                if comAttr['angle'] == permAttr['angle']:
                    totalVal = totalVal + 2;
            if ('fill' in comAttr) and ('fill' in permAttr):
                if comAttr['fill'] == permAttr['fill']:
                    totalVal = totalVal + 1;
        return (thisPair, totalVal);

    def getDictOfRelation(self, firstAttr, secondAttr):
        tempDict = {};

        dicts = self.chooseLargerDict(firstAttr, secondAttr);
        largerDict = dicts['larger'];
        smallerDict = dicts['smaller'];

        #TODO: fill out the rest of the attributes
        for attr, val1 in largerDict.items():
            newAttrKey = attr;
            newAttrVal = None;
            if attr in smallerDict:
                val2 = smallerDict[attr];
                if val1 == val2:
                    newAttrVal = 'Same';
                elif attr == 'shape':
                    newAttrVal = 'Changed';
                elif attr == 'fill':
                    filler = '';
                elif attr == 'size':
                    filler = '';
                elif attr == 'angle':
                    newAttrVal = self.angleChange(val1, val2);
                elif attr == 'inside':
                    filler = '';
                elif attr == 'alignment':
                    newAttrVal = self.alignmentChange(val1, val2);
                elif attr == 'above':
                    filler = '';
            tempDict[newAttrKey] = newAttrVal;

        return tempDict;

    def calculateSimilarValue(self, dict1, dict2):
        dicts = self.chooseLargerDict(dict1, dict2);
        largerDict = dicts['larger'];
        smallerDict = dicts['smaller'];

        count = 0;
        for attr in largerDict:
            if attr in smallerDict:
                if (largerDict[attr] == smallerDict[attr]):
                    count = count + 1;
        return count;

    def angleChange(self, valA, valB):
        value = None;
        intValA = int(valA);
        intValB = int(valB);

        if (((intValA > 180) and (intValB < 180)) or ((intValA < 180) and (intValB > 180))) and \
            ((intValA + intValB) is 360):
            value = 'Horizontal';
        elif (((intValA > 180) and (intValB > 180)) or ((intValA < 180) and (intValB < 180))) and \
            (((intValA % 180) + (intValB % 180)) is 180) or \
            ((intValA is 180) and (intValB is 0)) or ((intValA is 0) and (intValB is 180)):
            value = 'Vertical';
        elif (abs(intValA - intValB) is 180):
            value = 'Diagonal';
        else:
            value = 'Rotational';
        return value;

    #TODO: make sure that valA is from A or C, and valB is B or 1,2,3,4,5,6
    #TODO: make a up/down & left/right
    def alignmentChange(self, valA, valB):
        value = None;

        if ((valA == 'top-left') and (valB == 'top-right')) or ((valA == 'bottom-left') and (valB == 'bottom-right')):
            value = 'Right Shift';
        elif ((valA == 'top-right') and (valB == 'top-left')) or ((valA == 'bottom-right') and (valB == 'bottom-left')):
            value = 'Left Shift';
        elif ((valA == 'top-left') and (valB == 'bottom-left')) or ((valA == 'top-right') and (valB == 'bottom-right')):
            value = 'Down Shift';
        elif ((valA == 'bottom-left') and (valB == 'top-left')) or ((valA == 'bottom-right') and (valB == 'top-right')):
            value = 'Up Shift';
        elif ((valA == 'top-left') and (valB == 'bottom-right')) or ((valA == 'top-right') and (valB == 'bottom-left')):
            value = 'Diagonal Down Shift';
        elif ((valA == 'bottom-left') and (valB == 'top-right')) or ((valA == 'bottom-right') and (valB == 'top-right')):
            value = 'Diagonal Up Shift';
        return value;

    def changeInObjects(self, objs1, objs2):
        numOfObjs = ();
        if len(objs1) > len(objs2):
            numOfObjs = ('deleted', len(objs1) - len(objs2));
        elif len(objs2) > len(objs1):
            numOfObjs = ('added', len(objs2) - len(objs1));
        return numOfObjs;

    def chooseLargerDict(self, dict1, dict2):
        dicts = {};
        if len(dict1) >= len(dict2):
            dicts['larger'] = dict1;
            dicts['smaller'] = dict2;
        else:
            dicts['larger'] = dict2;
            dicts['smaller'] = dict1;
        return dicts;
