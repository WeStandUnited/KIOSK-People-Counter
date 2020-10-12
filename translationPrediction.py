import math

def most_likely_translation(current_object: ((float, float), float), previous_objects: ([(float, float)], [float])) -> (float, float):
    
    '''
    
    Description:
    
        Takes a single point in a frame and does a series of calculations to return the most likely point in the previous
        frame that the single point translated from.
    
    Parameters: 
        
        current_object:  ( (centroid's x position, centroid's y position), ROI's Area )
        previous_objects: ( [ (centroid's x position, centroid's y position) ], [ ROI's Area ] )
        
    Returns:
    
        A single point from a previous frame, where the current object translated from. 
    
    '''
    
    # Current Object being tracked
    current_point, current_area = current_object
    
    # All the previous objects in the previous frame
    previous_points, previous_area = previous_objects
    
    smallest_distance = -1
    smallest_distance_index = -1
    closest_ratio_difference_to_zero = -1
    closest_area_index = -1
    
    # Loop through each of the previous points to find:
        # 1) The vector with the smallest magnitude between two points
        # 2) The smallest difference is area between two bounding boxes
    for i in range(0, len(previous_points)):
        
        # Distance between two points
        distance = math.sqrt( (current_point[0] - previous_points[i][0]) ** 2)
        
        if smallest_distance_index != -1 and distance < smallest_distance:
            smallest_distance = distance
            smallest_distance_index = i
        
        if smallest_distance_index == -1:
            smallest_distance = distance
            smallest_distance_index = i
            
        # Calculates the difference between two areas and finds how close the values are too each other
        area_ratio = previous_area[i] / current_area
        ratio_difference = abs( 1 - area_ratio)
        
        if closest_area_index != -1 and ratio_difference < closest_ratio_difference_to_zero:
            closest_ratio_difference_to_zero = ratio_difference
            closest_area_index = i
            
        if closest_area_index == -1:
            closest_ratio_difference_to_zero = ratio_difference
            closest_area_index = i
    
    # If there is a point that has the smallest vector magnitude with respect to the current point
    # and there is a difference point that has the smallest difference is area then find the most probable
    # point that the current point translated from        
    if smallest_distance_index != closest_area_index:
        
        # Weights for most probable point equation
        distance_weight = 0.8
        area_ratio_weight = 0.1
        
        point_a_distance = math.sqrt( (current_point[0] - previous_points[smallest_distance_index][0]) ** 2 )
        point_a_area_ratio = previous_area[smallest_distance_index] / current_area
        point_a_ratio_difference = abs( 1 - point_a_area_ratio )
        
        point_b_distance = math.sqrt(( current_point[0] - previous_points[closest_area_index][0]) ** 2 )
        point_b_area_ratio = previous_area[closest_area_index] / current_area
        point_b_ratio_difference = abs( 1 - point_b_area_ratio )
        
        # Most probable point equations
       ##############################################################################################################################
        probability_mapping_to_a = ( distance_weight ) * ( point_a_distance ) - ( area_ratio_weight ) * ( point_a_ratio_difference )#
                                                                                                                                    #      
        probability_mapping_to_b = ( distance_weight ) * ( point_b_distance ) - ( area_ratio_weight ) * ( point_b_ratio_difference )#
       ############################################################################################################################## 
        
        # Which ever has a smaller value, then that is the most probable point 
        if probability_mapping_to_a < probability_mapping_to_b: most_probable_mapping_index = smallest_distance_index
        else: most_probable_mapping_index = closest_area_index
    
    # If there is a point that has the smallest vector magnitude and that same point also has the smallest difference in area
    # Then that point is the most probable point    
    else: 
        most_probable_mapping_index = smallest_distance_index
    
    # Returns a tuple (x, y)    
    return previous_points[most_probable_mapping_index]